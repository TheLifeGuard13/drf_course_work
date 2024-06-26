import json
from datetime import datetime, timedelta

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from users.models import User


def set_schedule_for_reminder(obj):
    """Создает периодическую задачу, принимает экземплял класса."""
    time = datetime.strptime(obj["execution_time"], "%H:%M:%S") - timedelta(minutes=15)
    telegram_chat_id = User.objects.get(id=obj["owner"]).tg_id
    message = f"Через 15 минут вам пора [{obj["action"]}],{telegram_chat_id}"

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=int(time.minute),
        hour=int(time.hour),
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
        timezone="Europe/Moscow",
    )

    PeriodicTask.objects.create(
        crontab=schedule,
        name=f"Sending reminder #{int(obj['id'])}",
        task="habbits.tasks.send_telegram_reminder",
        args=json.dumps([message]),
    )
