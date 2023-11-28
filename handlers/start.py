from vkbottle.bot import Message
from config import labeler, TOKEN, state_dispenser
import requests
from keyboards import confirmation, geoposition, main_keyboard
from states.registration import Reg
from utilites import db_commands


@labeler.message(text='Начать')
async def starting(message: Message):
    if not db_commands.check_user(user_id=message.from_id):
        await start_new_user(message)

    else:
        await message.answer(
            'Рад снова видеть тебя!',
            keyboard=main_keyboard
        )


@labeler.message(payload={'command': 'delete'})
async def start_new_user(message: Message):
    db_commands.add_user(user_id=message.from_id)
    city_request = requests.get(url='https://api.vk.com/method/users.get',
                                params={
                                    'access_token': TOKEN,
                                    'v': 5.131,
                                    'fields': 'city',
                                    'user_ids': message.from_id
                                }).json()['response'][0]
    if 'city' in city_request:
        await message.answer(f'Привет! Дай уточню, твой город {city_request["city"]["title"]}?',
                             keyboard=confirmation)
        db_commands.add_city(user_id=message.from_id, city=city_request['city']["title"])
    else:
        await message.answer(f'Привет! У тебя не указан город в профиле. Скажешь мне его?',
                             keyboard=geoposition)
        await state_dispenser.set(message.peer_id, Reg.USER_CITY)


@labeler.message(payload={'registration': 'yes'})
async def registration_yes(message: Message):
    await message.answer(f'Ура! Теперь я знаю твой город)',
                         keyboard=main_keyboard)


@labeler.message(payload={'registration': 'no'})
async def registration_no(message: Message):
    await message.answer(f'Понял. Тогда отправь мне свое гео)',
                         keyboard=geoposition)
    await state_dispenser.set(message.peer_id, Reg.USER_CITY)


@labeler.message(payload={'registration': 'place'}, state=Reg.USER_CITY)
async def registration_user_city(message: Message):
    db_commands.add_city(user_id=message.from_id, city=message.geo.place.city)

    await message.answer(f'Спасибо! Запомнил твой город)',
                         keyboard=main_keyboard)
