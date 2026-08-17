from django.contrib import admin
from .models import AIFormAnalysis


@admin.register(AIFormAnalysis)
class AIFormAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'exercise',
        'repetitions_detected',
        'form_score',
        'analysis_duration',
        'created_at',
    )

    search_fields = (
        'user__username',
        'exercise__exercise_name',
    )

    list_filter = ('exercise',)