from vkbottle.bot import Message
from config import labeler, state_dispenser, WEATHER_TOKEN
from keyboards import dayweek, main_keyboard
from states.weather_states import Weather
import requests
from utilites import db_commands


@labeler.message(payload={'command': 'weather'})
async def weather_select(message: Message):
    """Выбор пользователем дня. Сегодня или завтра"""

    await message.answer(
        'Хорошо! Только для начала давай определимся:\n\n'
        'Тебе на сегодня или на завтра?',
        keyboard=dayweek
    )
    await state_dispenser.set(message.peer_id, Weather.DATE)


@labeler.message(state=Weather.DATE,
                 payload=[{'dayweek': 'today'}, {'dayweek': 'tomorrow'}])
async def weather_sent(message: Message):

    day = 'Сегодня' if message.payload == '{"dayweek":"today"}' else 'Завтра'
    weather = weather_get(message.from_id)[day]

    if weather:
        await message.answer(
            f'{day} в городе {db_commands.get_user_city(user_id=message.from_id)[0]} '
            f'{weather["weather"][0]["description"]}.\n'
            f'Температура в среднем будет около {round(weather["main"]["temp"])} грудусов',
            keyboard=main_keyboard
        )

    else:
        await message.answer(
            f'Не получилось узнать погоду :(',
            keyboard=main_keyboard)

    await state_dispenser.delete(message.peer_id)


def weather_get(user_id):
    """Запрос актуальных данных о погоде"""

    weather_request = requests.get(
        url=f'https://api.openweathermap.org/data/2.5/forecast',
        params={
            'q': db_commands.get_user_city(user_id=user_id)[0],
            'lang': 'ru',
            'cnt': 2,
            'units': 'metric',
            'appid': WEATHER_TOKEN
        }
    ).json()
    if weather_request['cod'] == '200':
        return {
            'Сегодня': weather_request['list'][0],
            'Завтра': weather_request['list'][1]
        }
