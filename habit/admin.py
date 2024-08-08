from django.contrib import admin
from habit.models import Habits


@admin.register(Habits)
class HabitsAdmin(admin.ModelAdmin):
    list_display = ["pk", "owner", "place", "time", "action"]
