from django.db import models
from django.conf import settings


class FitnessProfile(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    FITNESS_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('very_active', 'Very Active'),
        ('athlete', 'Athlete'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fitness_profile'
    )

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    height = models.FloatField(
        help_text='Height in centimeters'
    )

    weight = models.FloatField(
        help_text='Weight in kilograms'
    )

    fitness_level = models.CharField(
        max_length=20,
        choices=FITNESS_LEVEL_CHOICES
    )

    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES
    )

    equipment_available = models.TextField(
        blank=True,
        help_text='Example: Dumbbells, Resistance Bands, None'
    )

    workout_duration = models.PositiveIntegerField(
        help_text='Preferred workout duration in minutes'
    )

    workout_days = models.PositiveIntegerField(
        help_text='Number of workout days per week'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username}'s Fitness Profile"


class FitnessGoal(models.Model):

    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_building', 'Muscle Building'),
        ('strength', 'Strength'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('general_fitness', 'General Fitness'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fitness_goal'
    )

    goal = models.CharField(
        max_length=30,
        choices=GOAL_CHOICES
    )

    target_weight = models.FloatField(
        null=True,
        blank=True,
        help_text='Target weight in kilograms'
    )

    target_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_goal_display()}"


class FitnessAssessment(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fitness_assessment'
    )

    bmi = models.FloatField()

    bmr = models.FloatField()

    daily_calories = models.FloatField()

    fitness_level = models.CharField(
        max_length=20
    )

    assessment_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - Fitness Assessment"