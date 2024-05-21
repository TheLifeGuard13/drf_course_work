from django.urls import path
from rest_framework.routers import DefaultRouter

from habbits.apps import HabbitsConfig
from habbits.views import HabitListAPIView, HabitViewSet

app_name = HabbitsConfig.name

router = DefaultRouter()
router.register(r"habbits", HabitViewSet, basename="habbits")

urlpatterns = [
    path("public/", HabitListAPIView.as_view(), name="public_habits_list"),
] + router.urls
