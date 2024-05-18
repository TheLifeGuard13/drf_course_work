from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from habbits.models import Habit
from habbits.validators import DurationValidator, PeriodValidator


class HabitSerializer(serializers.ModelSerializer):
    validators = [DurationValidator(field="execution_duration_seconds"), PeriodValidator(field="periodicity")]
    # connected_habits = SerializerMethodField()

    # def get_connected_habits(self, obj):
    #     habits = obj.useful_habits.filter(is_pleasant=True)
    #     return habits

    def validate(self, data):
        if data.get('award') and data.get('connected_habits') is not None:
            raise serializers.ValidationError("Может быть выбрано вознаграждение или связанная привычка.")
        if data.get("is_pleasant"):
            if data.get('award') or data.get('connected_habits') is not None:
                raise serializers.ValidationError("У полезной привычки нет вознаграждения или связанной привычки.")
        return data

    class Meta:
        model = Habit
        fields = "__all__"
