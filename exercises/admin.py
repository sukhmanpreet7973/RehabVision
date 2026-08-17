from django.contrib import admin
from .models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'exercise_name',
        'target_muscle',
        'equipment',
        'difficulty',
        'created_at',
    )

    search_fields = (
        'exercise_name',
        'target_muscle',
        'equipment',
    )

    list_filter = (
        'difficulty',
        'equipment',
    )