from django.contrib import admin
from .models import WeightRecord, ProgressRecord


@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'weight',
        'recorded_date',
    )

    search_fields = ('user__username',)

    list_filter = ('recorded_date',)


@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date',
        'workouts_completed',
        'total_workout_minutes',
        'calories_burned',
        'total_repetitions',
        'average_performance_score',
        'goal_completion_percentage',
    )

    search_fields = ('user__username',)

    list_filter = ('date',)