from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitsListAPIView, HabitsRetrieveAPIView, HabitsCreateAPIView, HabitsUpdateAPIView, \
    HabitsDestroyAPIView, HabitsPublicListAPIView

app_name = HabitConfig.name

urlpatterns = [
    path("habits/list/", HabitsListAPIView.as_view(), name="habits_list"),
    path("habits/<int:pk>/", HabitsRetrieveAPIView.as_view(), name="habits_retrieve"),
    path("habits/create/", HabitsCreateAPIView.as_view(), name="habits_create"),
    path("habits/update/<int:pk>/", HabitsUpdateAPIView.as_view(), name="habits_update"),
    path("habits/delete/<int:pk>/", HabitsDestroyAPIView.as_view(), name="habits_delete"),
    path("habits/public/", HabitsPublicListAPIView.as_view(), name="public_list"),
]
