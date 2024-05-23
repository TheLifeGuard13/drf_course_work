# Generated by Django 5.0.6 on 2024-05-23 16:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habbits", "0013_alter_habit_periodicity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="execution_date",
            field=models.DateField(default=datetime.date(2024, 5, 24), verbose_name="Дата начала выполнения привычки"),
        ),
    ]