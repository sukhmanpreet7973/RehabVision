from django.db import models
from django.contrib.auth.models import User


class Reminder(models.Model):

    REMINDER_TYPE_CHOICES = [
        ('workout', 'Workout'),
        ('water', 'Water'),
        ('meal', 'Meal'),
        ('weigh_in', 'Weight Check'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reminders'
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    reminder_type = models.CharField(
        max_length=20,
        choices=REMINDER_TYPE_CHOICES
    )

    reminder_time = models.TimeField()

    reminder_date = models.DateField(
        null=True,
        blank=True
    )

    is_recurring = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.title}"