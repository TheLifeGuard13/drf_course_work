from rest_framework import generics, viewsets

from habbits.models import Habit
from habbits.paginators import HabitPaginator
from habbits.serializers import HabitSerializer
from users.permissions import IsOwner, IsStaff


# Список публичных привычек.
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

    def get_permissions(self):
        if self.action in ["list", "create", "update", "retrieve", "destroy"]:
            self.permission_classes = (IsOwner | IsStaff, )
        return super().get_permissions()
