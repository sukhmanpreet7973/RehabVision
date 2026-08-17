from django.contrib import admin
from .models import AssessmentHistory


@admin.register(AssessmentHistory)
class AssessmentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'weight',
        'height',
        'bmi',
        'bmr',
        'daily_calories',
        'fitness_level',
        'assessment_date',
    )

    search_fields = ('user__username',)
    list_filter = ('fitness_level',)