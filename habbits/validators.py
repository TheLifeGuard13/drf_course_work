from rest_framework.exceptions import ValidationError


class DurationValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value) -> None:
        temp_value = dict(value).get(self.field)
        allowed_duration = 120
        if int(temp_value) >= allowed_duration:
            raise ValidationError(f"Время выполнения должно быть не больше 120 секунд")


class PeriodValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value) -> None:
        temp_value = dict(value).get(self.field)
        if not 0 < int(temp_value) <= 7:
            raise ValidationError(f"Частота выполнения привычки не менее 1 и не более 7 раз в неделю")
