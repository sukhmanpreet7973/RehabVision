from django.db import models
from django.contrib.auth.models import User


class AssessmentHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assessment_history'
    )

    weight = models.FloatField(
        help_text='Weight in kilograms'
    )

    height = models.FloatField(
        help_text='Height in centimeters'
    )

    bmi = models.FloatField()

    bmr = models.FloatField()

    daily_calories = models.FloatField()

    fitness_level = models.CharField(
        max_length=30
    )

    assessment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.assessment_date.date()}"
        )
