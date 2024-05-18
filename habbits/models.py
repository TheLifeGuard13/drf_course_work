from django.conf import settings
from django.db import models

from config.settings import NULLABLE


class Habit(models.Model):
    """
    Модель Привычки
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE, **NULLABLE, verbose_name="Владелец")
    execution_time = models.DateTimeField(verbose_name="Дата выполнения")
    action = models.CharField(max_length=150, verbose_name="Действие")
    execution_duration_seconds = models.IntegerField(verbose_name="Время выполнения (в секундах)")

    place = models.CharField(max_length=150, **NULLABLE, verbose_name="Место")
    award = models.CharField(max_length=150, **NULLABLE, verbose_name="Вознаграждение")
    periodicity = models.SmallIntegerField(default=1, verbose_name="Периодичность в неделю")
    connected_habits = models.ForeignKey("self", **NULLABLE, on_delete=models.SET,
                                         related_name="useful_habits", verbose_name="Приятные привычки")

    is_pleasant = models.BooleanField(default=False, verbose_name="Приятность")
    is_shared = models.BooleanField(default=False, verbose_name="Публичность")
    picture = models.ImageField(upload_to="pictures/", **NULLABLE, verbose_name="Картинка")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self) -> str:
        return f"{self.action}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"






