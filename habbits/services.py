import requests

from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_URL


def telegram_api(message: str) -> None:
    """
    Функция отправки сообщения в Телеграм бот
    """
    requests.get(f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}')
