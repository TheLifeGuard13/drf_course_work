from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habbits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test_email", is_staff=True, is_superuser=True, password="123")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            action="Сделать 500 приседаний",
            execution_time="01:00:00",
            execution_duration_seconds=120,
            is_shared=True,
            execution_date="2024-12-31",
            owner=self.user,
        )

    def test_list_public_habits(self):
        """Тестирование вывода списка публичных привычек"""
        url = reverse("habbits:public_habits_list")
        response = self.client.get(url)
        data = response.json()
        data["results"][0].pop("created")  # убираем автогенерируемую дату

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.id,
                    "execution_time": self.habit.execution_time,
                    "action": self.habit.action,
                    "execution_duration_seconds": self.habit.execution_duration_seconds,
                    "place": None,
                    "award": None,
                    "periodicity": self.habit.periodicity,
                    "is_pleasant": False,
                    "is_shared": True,
                    "picture": None,
                    "execution_date": self.habit.execution_date,
                    "owner": self.user.pk,
                    "connected_habit": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        data = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": self.habit.execution_duration_seconds,
            "periodicity": self.habit.periodicity,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
        }

        response = self.client.post("/habbits/", data=data)
        data = response.json()
        data.pop("created")  # убираем автогенерируемую дату
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            data,
            {
                "id": response.json().get("id"),
                "execution_time": "01:00:00",
                "action": "Сделать 500 приседаний",
                "execution_duration_seconds": 120,
                "place": None,
                "award": None,
                "periodicity": 7,
                "is_pleasant": False,
                "is_shared": False,
                "picture": None,
                "execution_date": "2024-12-31",
                "owner": self.user.pk,
                "connected_habit": None,
            },
        )
        self.assertTrue(Habit.objects.all().exists())

    def test_retrieve_habit(self):
        """Тестирование вывода отдельной привычки"""
        response = self.client.get(f"/habbits/{self.habit.pk}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_delete_course(self):
        """Тестирование удаления привычки"""
        response = self.client.delete(f"/habbits/{self.habit.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_patch_habit(self):
        """Тестирование обновления привычки"""
        data = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": 100,
            "periodicity": self.habit.periodicity,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
        }
        response = self.client.patch(f"/habbits/{self.habit.pk}/", data=data)

        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("execution_duration_seconds"), 100)

    def test_create_habit_wrong_period(self):
        """Тестирование создания привычки с ошибкой в периодичности"""
        data = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": self.habit.execution_duration_seconds,
            "periodicity": 10,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
        }

        response = self.client.post("/habbits/", data=data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result, {"non_field_errors": ["Частота выполнения привычки не менее 1 и не более 7 раз в неделю"]}
        )

    def test_create_habit_wrong_start_date(self):
        """Тестирование создания привычки с ошибкой в дате старта"""
        data = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": self.habit.execution_duration_seconds,
            "periodicity": self.habit.periodicity,
            "execution_date": "2023-12-31",
            "owner": self.user.pk,
        }

        response = self.client.post("/habbits/", data=data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result, {"non_field_errors": ["Давайте лучше с завтрашнего дня!"]})

    def test_create_habit_wrong_duration(self):
        """Тестирование создания привычки с ошибкой в дате старта"""
        data = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": 300,
            "periodicity": self.habit.periodicity,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
        }

        response = self.client.post("/habbits/", data=data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result, {"non_field_errors": ["Время выполнения должно быть не больше 120 секунд"]})

    def test_create_habit_connected_habit(self):
        """Тестирование создания привычки с попыткой связать полезную привычку"""
        data = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": self.habit.execution_duration_seconds,
            "periodicity": self.habit.periodicity,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
            "connected_habit": self.habit.id,
        }

        response = self.client.post("/habbits/", data=data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result, {"non_field_errors": ["Нельзя сделать полезную привычку связанной"]})

    def test_create_habit_pleasant_award(self):
        """Тестирование создания привычки с попыткой указать вознаграждение за приятную привычку"""
        data = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": self.habit.execution_duration_seconds,
            "periodicity": self.habit.periodicity,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
            "is_pleasant": True,
            "award": "Покурить",
        }

        response = self.client.post("/habbits/", data=data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result, {"non_field_errors": ["У полезной привычки нет вознаграждения или связанной привычки."]}
        )

    def test_create_habit_award_and_habit(self):
        """Тестирование создания привычки с попыткой указать и вознаграждение и связанную привычку"""
        first_habit = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": self.habit.execution_duration_seconds,
            "periodicity": self.habit.periodicity,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
            "is_pleasant": True,
        }
        first_response = self.client.post("/habbits/", data=first_habit)
        first_id = first_response.json().get("id")

        data_two = {
            "execution_time": self.habit.execution_time,
            "action": self.habit.action,
            "execution_duration_seconds": self.habit.execution_duration_seconds,
            "periodicity": self.habit.periodicity,
            "execution_date": self.habit.execution_date,
            "owner": self.user.pk,
            "is_pleasant": False,
            "award": "Покурить",
            "connected_habit": first_id,
        }

        second_response = self.client.post("/habbits/", data=data_two)
        result = second_response.json()
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result, {"non_field_errors": ["Может быть указано только вознаграждение или связанная привычка."]}
        )
