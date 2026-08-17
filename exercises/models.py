from django.db import models


class Exercise(models.Model):

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    MOVEMENT_TYPE_CHOICES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('mobility', 'Mobility'),
        ('balance', 'Balance'),
        ('core', 'Core'),
    ]

    exercise_name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    target_muscle = models.CharField(
        max_length=200
    )

    equipment = models.CharField(
        max_length=100,
        default='None'
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES
    )

    movement_type = models.CharField(
        max_length=30,
        choices=MOVEMENT_TYPE_CHOICES
    )

    instructions = models.TextField()

    common_mistakes = models.TextField(
        blank=True
    )

    safety_tips = models.TextField(
        blank=True
    )

    # Exercise demonstration
    demonstration_image = models.ImageField(
        upload_to='exercise_images/',
        blank=True,
        null=True
    )

    demonstration_animation = models.FileField(
        upload_to='exercise_animations/',
        blank=True,
        null=True
    )

    demonstration_url = models.URLField(
        blank=True
    )

    # Workout recommendations
    recommended_sets = models.PositiveIntegerField(
        default=3
    )

    recommended_repetitions = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    recommended_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Duration in seconds'
    )

    rest_seconds = models.PositiveIntegerField(
        default=60
    )

    # Future AI information
    ai_exercise_code = models.CharField(
        max_length=50,
        blank=True,
        help_text='Example: squat, pushup, lunge'
    )

    primary_joints = models.CharField(
        max_length=200,
        blank=True,
        help_text='Example: knee, hip, ankle'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.exercise_name