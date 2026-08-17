from django.db import models
from django.contrib.auth.models import User


class WeightRecord(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='weight_records'
    )

    weight = models.FloatField(
        help_text='Weight in kilograms'
    )

    recorded_date = models.DateField()

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-recorded_date']

    def __str__(self):
        return f"{self.user.username} - {self.weight} kg"


class ProgressRecord(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )

    date = models.DateField()

    workouts_completed = models.PositiveIntegerField(
        default=0
    )

    total_workout_minutes = models.PositiveIntegerField(
        default=0
    )

    calories_burned = models.FloatField(
        default=0
    )

    total_repetitions = models.PositiveIntegerField(
        default=0
    )

    average_performance_score = models.FloatField(
        default=0
    )

    goal_completion_percentage = models.FloatField(
        default=0
    )

    def __str__(self):
        return f"{self.user.username} - {self.date}"