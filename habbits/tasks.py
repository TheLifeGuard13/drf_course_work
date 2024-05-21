import requests
from celery import shared_task

from config.settings import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, TELEGRAM_URL
from habbits.models import Habit


@shared_task
def send_telegram_start_message_award(obj):
    """Отправляет сообщение, если выбрано вознаграждение."""
    message = (
        f"Вы запланировали привычку [{obj["action"]}]! "
        f"в [{obj["execution_time"]}] в [{obj["place"]}], "
        f"[{obj["periodicity"]}] раз в неделю! "
        f"Вознаграждение [{obj["award"]}]"
    )
    requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}")


@shared_task
def send_telegram_start_message_connected_habit(obj):
    """Отправляет сообщение, если выбрана связанная привычка."""
    con_habit = Habit.objects.get(id=obj["connected_habit"])
    message = (
        f"Вы запланировали привычку [{obj["action"]}]! "
        f"в [{obj["execution_time"]}] в [{obj["place"]}], "
        f"[{obj["periodicity"]}] раз в неделю! "
        f"Связанная привычка [{con_habit.action}]"
    )
    requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}")


@shared_task
def send_telegram_start_message(obj):
    """Отправляет сообщение, если не выбрано вознаграждение и связанная привычка."""
    message = (
        f"Вы запланировали привычку [{obj["action"]}]! "
        f"в [{obj["execution_time"]}] в [{obj["place"]}], "
        f"[{obj["periodicity"]}] раз в неделю!"
    )
    requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}")


@shared_task
def send_telegram_reminder(message):
    """Отправляет уведомление за 15 минут до времени выполнения привычки."""
    requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}")
