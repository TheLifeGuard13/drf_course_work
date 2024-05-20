from datetime import datetime

from rest_framework.exceptions import ValidationError

from habbits.models import Habit


class DurationValidator:
    """Валидирует поле - время выполнения."""
    def __init__(self, field):
        self.field = field

    def __call__(self, value) -> None:
        temp_value = dict(value).get(self.field)
        allowed_duration = 120
        if int(temp_value) > allowed_duration:
            raise ValidationError(f"Время выполнения должно быть не больше 120 секунд")


class PeriodValidator:
    """Валидирует поле - периодичность выполнения."""
    def __init__(self, field):
        self.field = field

    def __call__(self, value) -> None:
        temp_value = dict(value).get(self.field)
        if not 0 < int(temp_value) <= 7:
            raise ValidationError(f"Частота выполнения привычки не менее 1 и не более 7 раз в неделю")


class ConnectedHabitValidator:
    """Валидирует поле - связанная привычка (запрещает связывать полезную привычку с полезной)."""
    def __init__(self, field):
        self.field = field

    def __call__(self, value) -> None:
        if value["connected_habit"]:
            connected_habit_id = value.get('connected_habit').id
            connected_habit = Habit.objects.get(id=connected_habit_id)

            if not connected_habit.is_pleasant:
                raise ValidationError(f"Нельзя сделать полезную привычку связанной")


class StartHabitValidator:
    """Валидирует поле - дата старта привычки (с завтрашнего дня)."""
    def __init__(self, field):
        self.field = field

    def __call__(self, value) -> None:
        temp_value = dict(value).get(self.field)
        now = datetime.now().date()
        if temp_value <= now:
            raise ValidationError(f"Давайте лучше с завтрашнего дня!")
