from vkbottle.bot import Message
from config import labeler, state_dispenser, AFISHA_CITY
from keyboards import dayweek, main_keyboard
from states.afisha_states import Afisha
import requests
import datetime
import time
from utilites import db_commands


@labeler.message(payload={'command': 'afisha'})
async def afisha_select(message: Message):
    """Выбор пользователем дня. Сегодня или завтра"""

    await message.answer(
        'Уф! Сегодня многое намечается)\n\n'
        'Или тебе афишу на завтра показать?',
        keyboard=dayweek
    )
    await state_dispenser.set(message.peer_id, Afisha.DATE)


@labeler.message(state=Afisha.DATE,
                 payload=[{'dayweek': 'today'}, {'dayweek': 'tomorrow'}])
async def afisha_sent(message: Message):
    """Преобразование результата функций в сообщение пользователю"""

    tomorrow = False if message.payload == '{"dayweek":"today"}' else True
    afisha = afisha_get(message.from_id, tomorrow=tomorrow)

    if afisha:
        await message.answer(
            '\n---\n'.join(
                f"{event['short_title']}\n"
                f"Цена: {event['price']}\n"
                f"{event['site_url']}" for event in afisha),
            keyboard=main_keyboard
        )

    else:
        await message.answer(
            f'В твоем городе не получилось найти афишу :(',
            keyboard=main_keyboard)

    await state_dispenser.delete(message.peer_id)


def afisha_get(user_id, tomorrow=False):
    """Функция запроса актуальной афиши"""

    day_from = datetime.datetime.today()  # начало промежутка для поиска
    user_city = db_commands.get_user_city(user_id=user_id)[0].lower()  # запрос города из БД
    if tomorrow:
        day_from += datetime.timedelta(days=1)
    day_to = day_from + datetime.timedelta(days=1)  # конец промежутка поиска

    afisha_request = requests.get(url='https://kudago.com/public-api/v1.4/events/',
                                  params={
                                      'page_size': 5,
                                      'lang': 'ru',
                                      'location': AFISHA_CITY[user_city],
                                      'actual_since': time.mktime(day_from.timetuple()),
                                      'actual_until': time.mktime(day_to.timetuple()),
                                      'categories': '-exhibition,cinema,theater',
                                      'fields': 'title,short_title,price,site_url'
                                  }).json()
    if 'detail' not in afisha_request:
        return afisha_request['results']
