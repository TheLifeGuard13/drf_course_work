from rest_framework import generics, viewsets

from habbits.models import Habit
from habbits.paginators import HabitPaginator
from habbits.serializers import HabitSerializer
from habbits.services import set_schedule_for_reminder
from habbits.tasks import (
    send_telegram_start_message,
    send_telegram_start_message_award,
    send_telegram_start_message_connected_habit,
)
from users.permissions import IsOwner, IsStaff


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_shared=True)


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(owner=user)

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()
        if habit.award:
            send_telegram_start_message_award.delay(serializer.data)  # отправляет сообщение сразу
        elif habit.connected_habit:
            send_telegram_start_message_connected_habit.delay(serializer.data)  # отправляет сообщение сразу
        else:
            send_telegram_start_message.delay(serializer.data)  # отправляет сообщение сразу
        set_schedule_for_reminder(serializer.data)  # запускает планировщика

    def get_permissions(self):
        if self.action in ["list", "create", "update", "retrieve", "destroy"]:
            self.permission_classes = (IsOwner | IsStaff,)
        return super().get_permissions()
