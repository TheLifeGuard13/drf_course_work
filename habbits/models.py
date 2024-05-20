import datetime

from django.conf import settings
from django.db import models

from config.settings import NULLABLE


class Habit(models.Model):
    """
    Модель Привычки
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE, **NULLABLE,
                              verbose_name="Владелец")
    execution_time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=150, verbose_name="Действие")
    execution_duration_seconds = models.IntegerField(verbose_name="Время выполнения (в секундах)")

    place = models.CharField(max_length=150, **NULLABLE, verbose_name="Место")
    award = models.CharField(max_length=150, **NULLABLE, verbose_name="Вознаграждение")
    periodicity = models.SmallIntegerField(default=1, verbose_name="Периодичность в неделю")
    connected_habit = models.ForeignKey("self", **NULLABLE, on_delete=models.SET,
                                        related_name="useful_habit", verbose_name="Приятная привычка")

    is_pleasant = models.BooleanField(default=False, verbose_name="Приятность")
    is_shared = models.BooleanField(default=False, verbose_name="Публичность")
    picture = models.ImageField(upload_to="pictures/", **NULLABLE, verbose_name="Картинка")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    execution_date = models.DateField(default=datetime.datetime.now().date()+datetime.timedelta(days=1),
                                      verbose_name="Дата начала выполнения привычки")

    def __str__(self) -> str:
        return (f"{self.owner}, {self.execution_time}, {self.action}, {self.execution_duration_seconds},"
                f"{self.place}, {self.award}, {self.periodicity}, {self.connected_habit},"
                f"{self.is_pleasant}, {self.is_shared}, {self.picture}")

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"






