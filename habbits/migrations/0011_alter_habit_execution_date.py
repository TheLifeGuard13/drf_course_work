# Generated by Django 5.0.6 on 2024-05-20 16:56

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habbits", "0010_habit_execution_date_alter_habit_execution_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="execution_date",
            field=models.DateField(default=datetime.date(2024, 5, 21), verbose_name="Дата начала выполнения привычки"),
        ),
    ]
