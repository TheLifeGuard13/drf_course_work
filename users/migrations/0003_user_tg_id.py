# Generated by Django 5.0.6 on 2024-05-23 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_username_user_avatar_user_city_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tg_id",
            field=models.CharField(blank=True, default=0, max_length=15, null=True, verbose_name="Чат айди телеграмм"),
        ),
    ]