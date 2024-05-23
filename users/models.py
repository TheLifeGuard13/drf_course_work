from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")

    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name="Аватар")
    city = models.CharField(max_length=50, **NULLABLE, verbose_name="Город")
    tg_id = models.CharField(max_length=15, **NULLABLE, default=0, verbose_name="Чат айди телеграмм")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
