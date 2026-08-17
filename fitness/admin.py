from django.contrib import admin
from .models import FitnessProfile, FitnessGoal, FitnessAssessment


@admin.register(FitnessProfile)
class FitnessProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'age',
        'gender',
        'height',
        'weight',
        'fitness_level',
        'activity_level',
        'workout_days',
    )
    search_fields = ('user__username', 'user__email')
    list_filter = ('fitness_level', 'activity_level', 'gender')


@admin.register(FitnessGoal)
class FitnessGoalAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'goal',
        'target_weight',
        'target_date',
        'created_at',
    )
    search_fields = ('user__username',)
    list_filter = ('goal',)


@admin.register(FitnessAssessment)
class FitnessAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'bmi',
        'bmr',
        'daily_calories',
        'fitness_level',
        'assessment_date',
    )
    search_fields = ('user__username',)
    list_filter = ('fitness_level',)