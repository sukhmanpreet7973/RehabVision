from django.db import models
from django.contrib.auth.models import User


class DietPlan(models.Model):

    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_building', 'Muscle Building'),
        ('maintenance', 'Maintenance'),
        ('general_fitness', 'General Fitness'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diet_plans'
    )

    plan_name = models.CharField(
        max_length=150
    )

    goal = models.CharField(
        max_length=30,
        choices=GOAL_CHOICES
    )

    daily_calories = models.FloatField()

    protein_grams = models.FloatField()

    carbohydrate_grams = models.FloatField()

    fat_grams = models.FloatField()

    water_liters = models.FloatField(
        default=2.0
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.plan_name}"


class Meal(models.Model):

    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner'),
    ]

    diet_plan = models.ForeignKey(
        DietPlan,
        on_delete=models.CASCADE,
        related_name='meals'
    )

    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES
    )

    meal_name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    calories = models.FloatField()

    protein = models.FloatField()

    carbohydrates = models.FloatField()

    fat = models.FloatField()

    serving_size = models.CharField(
        max_length=100,
        blank=True
    )

    meal_time = models.TimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.diet_plan.user.username} - {self.meal_name}"