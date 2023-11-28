import schedule
import requests
import time
import config


def timetable_polling():
    schedule.every(15).minutes.do(get_token_alfacrm)
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_token_alfacrm():
    request = requests.post(url='https://umschool.s20.online/v2api/auth/login',
                            json={'email': config.CRM_EMAIL,
                                  'api_key': config.CRM_APIKEY})

    config.crm_token = request.json()['token']
