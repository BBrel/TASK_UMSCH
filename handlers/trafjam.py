from vkbottle.bot import Message
from config import labeler
from .weather import weather_get
from bs4 import BeautifulSoup
import requests
import fake_useragent


@labeler.message(payload={'command': 'trafjam'})
async def trafjam_sent(message: Message):
    await message.answer(
        'Проанализировав погоду в твоем городе, могу предположить, '
        f'что в это время балл пробок может достичь {trafjam_predict(message.from_id)}'
    )


def trafjam_predict(user_id):
    time = get_time_hour(user_id)
    weather = weather_get(user_id)['Сегодня']
    coof = 1
    scale = 2
    if weather and time:
        if 8 <= time <= 10 or 17 <= time <= 19:
            coof += 1.5
        if weather['weather'][0]['main'] in ['Snow', 'Rain']:
            coof += 1.5

    return round(scale*coof)


def get_time_hour(user_id):
    user = fake_useragent.UserAgent().random
    time_request = requests.get(
        url=f'https://time.is/ru/{"казань"}',
        headers={'User-Agent': user})

    soup = BeautifulSoup(time_request.text, "html.parser")
    time_hour = soup.find(id='clock').get_text()[:2]
    return int(time_hour)
