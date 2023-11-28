from vkbottle.bot import Message
from config import labeler

from bs4 import BeautifulSoup
import requests
import fake_useragent


@labeler.message(payload={'command': 'money'})
async def currency_sent(message: Message):
    """Обработка полученного результата и отправка пользователю"""

    await message.answer('\n\n'.join(
        f'{params["nom"]}{char} - {params["vinit"]}' for char, params in currency_get().items()))


def currency_get():
    """Запрос актуальной информации"""

    curr_request = requests.get(
        url=f'https://www.cbr-xml-daily.ru/daily.xml',
        headers={'User-Agent': fake_useragent.UserAgent().random}
    )
    soup = BeautifulSoup(curr_request.text, "xml")

    charcodes = soup.find_all('CharCode')[:5]  # поиск обозначений валюты
    nominals = soup.find_all('Nominal')[:5]  # поиск номинала валюты
    vunitrates = soup.find_all('VunitRate')[:5]  # поиск стоимости валюты

    result = {}

    # создание словаря с первыми 5ю валютами
    for num in range(5):
        result[charcodes[num].get_text()] = {
            'nom': nominals[num].get_text(),
            'vinit': vunitrates[num].get_text()
        }
    return result
