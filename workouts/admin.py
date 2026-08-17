from django.contrib import admin
from .models import (
    WorkoutPlan,
    WorkoutDay,
    WorkoutExercise,
    WorkoutSession,
    ExerciseRecord,
)


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'plan_name',
        'goal',
        'difficulty',
        'duration',
        'start_date',
        'is_active',
    )

    search_fields = (
        'user__username',
        'plan_name',
    )

    list_filter = (
        'goal',
        'difficulty',
        'is_active',
    )


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = (
        'workout_plan',
        'day_number',
        'day_name',
        'focus_area',
        'is_rest_day',
    )

    list_filter = ('is_rest_day',)


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'workout_day',
        'exercise',
        'sets',
        'repetitions',
        'duration_seconds',
        'rest_seconds',
        'order',
    )

    list_filter = ('exercise',)


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date',
        'duration_minutes',
        'calories_burned',
        'status',
        'difficulty_rating',
    )

    search_fields = ('user__username',)

    list_filter = (
        'status',
        'date',
    )


@admin.register(ExerciseRecord)
class ExerciseRecordAdmin(admin.ModelAdmin):
    list_display = (
        'workout_session',
        'exercise',
        'sets_completed',
        'repetitions_completed',
        'calories_burned',
        'performance_score',
    )

    list_filter = ('exercise',)