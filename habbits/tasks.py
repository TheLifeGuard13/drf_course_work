from celery import shared_task
from habbits.services import telegram_api

text = "Работай"


@shared_task
def send_telegram_reminder():
    telegram_api(text)
