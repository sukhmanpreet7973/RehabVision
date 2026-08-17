from django.db import models
from django.contrib.auth.models import User
from workouts.models import WorkoutSession
from exercises.models import Exercise


class AIFormAnalysis(models.Model):

    workout_session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name='ai_analyses'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_form_analyses'
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE
    )

    repetitions_detected = models.PositiveIntegerField(
        default=0
    )

    form_score = models.FloatField(
        default=0
    )

    mistakes_detected = models.TextField(
        blank=True
    )

    feedback = models.TextField(
        blank=True
    )

    analysis_duration = models.FloatField(
        default=0,
        help_text='Analysis duration in seconds'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.exercise.exercise_name} - "
            f"{self.form_score}%"
        )