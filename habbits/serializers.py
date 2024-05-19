from rest_framework import serializers

from habbits.models import Habit
from habbits.validators import DurationValidator, PeriodValidator, ConnectedHabitValidator


class HabitSerializer(serializers.ModelSerializer):
    validators = [DurationValidator(field="execution_duration_seconds"), PeriodValidator(field="periodicity"),
                  ConnectedHabitValidator(field="connected_habit")]

    def validate(self, data):
        if data.get("is_pleasant"):
            if data.get('award') or data.get('connected_habit') is not None:
                raise serializers.ValidationError("У полезной привычки нет вознаграждения или связанной привычки.")
        if data.get('award') and data.get('connected_habit') is not None:
            raise serializers.ValidationError("Может быть указано только вознаграждение или связанная привычка.")
        return data

    class Meta:
        model = Habit
        fields = "__all__"
