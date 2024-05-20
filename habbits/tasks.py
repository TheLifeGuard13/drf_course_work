import requests
from celery import shared_task

from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


@shared_task
def send_telegram_start_message(obj):
    message = (f"Вы запланировали привычку >>>{obj["action"]}<<< "
               f"в >>>{obj["execution_time"]}<<< в >>>{obj["place"]}<<<,"
               f">>>{obj["periodicity"]}<<< раз в неделю")
    requests.get(f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}')


@shared_task
def send_telegram_reminder(message):
    requests.get(f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}')
