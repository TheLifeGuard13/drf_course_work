from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response

from habbits.models import Habit
from habbits.paginators import HabitPaginator
from habbits.serializers import HabitSerializer
from habbits.services import set_schedule_for_reminder
# from habbits.tasks import send_telegram_start_message
from users.permissions import IsOwner, IsStaff


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()
        # send_telegram_start_message.delay(serializer.data)
        set_schedule_for_reminder(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        habit = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        serializer = self.serializer_class(habit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # send_telegram_start_message.delay(serializer.data)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["list", "create", "update", "retrieve", "destroy"]:
            self.permission_classes = (IsOwner | IsStaff, )
        return super().get_permissions()
