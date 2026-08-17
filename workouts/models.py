from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise


class WorkoutPlan(models.Model):

    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_building', 'Muscle Building'),
        ('strength', 'Strength'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('general_fitness', 'General Fitness'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workout_plans'
    )

    plan_name = models.CharField(
        max_length=150
    )

    goal = models.CharField(
        max_length=50,
        choices=GOAL_CHOICES
    )

    difficulty = models.CharField(
        max_length=30,
        choices=DIFFICULTY_CHOICES
    )

    duration = models.PositiveIntegerField(
        help_text='Workout duration in minutes'
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

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.plan_name}"


class WorkoutDay(models.Model):

    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='workout_days'
    )

    day_number = models.PositiveIntegerField()

    day_name = models.CharField(
        max_length=50
    )

    focus_area = models.CharField(
        max_length=100
    )

    is_rest_day = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.workout_plan.plan_name} - Day {self.day_number}"


class WorkoutExercise(models.Model):

    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.CASCADE,
        related_name='exercises'
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE
    )

    sets = models.PositiveIntegerField()

    repetitions = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    rest_seconds = models.PositiveIntegerField(
        default=60
    )

    order = models.PositiveIntegerField()

    notes = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.workout_day} - {self.exercise.exercise_name}"


class WorkoutSession(models.Model):

    SESSION_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workout_sessions'
    )

    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )

    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )

    date = models.DateField()

    start_time = models.DateTimeField(
        null=True,
        blank=True
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    duration_minutes = models.PositiveIntegerField(
        default=0
    )

    calories_burned = models.FloatField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=SESSION_STATUS_CHOICES,
        default='scheduled'
    )

    difficulty_rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='User rating from 1 to 5'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class ExerciseRecord(models.Model):

    workout_session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name='exercise_records'
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE
    )

    sets_completed = models.PositiveIntegerField(
        default=0
    )

    repetitions_completed = models.PositiveIntegerField(
        default=0
    )

    duration_seconds = models.PositiveIntegerField(
        default=0
    )

    calories_burned = models.FloatField(
        default=0
    )

    performance_score = models.FloatField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.workout_session.user.username} - "
            f"{self.exercise.exercise_name}"
        )