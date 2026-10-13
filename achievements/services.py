from django.utils import timezone

from .models import Achievement, UserAchievement, Streak
from workouts.models import WorkoutSession


def update_streak_and_achievements(user):
    today = timezone.localdate()

    # ----------------------------------------
    # UPDATE STREAK
    # ----------------------------------------

    streak, created = Streak.objects.get_or_create(user=user)

    if streak.last_workout_date == today:
        # Already completed a workout today
        pass

    elif streak.last_workout_date == today - timezone.timedelta(days=1):
        # Workout completed yesterday → continue streak
        streak.current_streak += 1

    else:
        # New streak
        streak.current_streak = 1

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.last_workout_date = today
    streak.save()

    # ----------------------------------------
    # COUNT COMPLETED WORKOUTS
    # ----------------------------------------

    completed_count = WorkoutSession.objects.filter(
        user=user,
        status='completed'
    ).count()

    # ----------------------------------------
    # AUTOMATIC ACHIEVEMENTS
    # ----------------------------------------

    achievement_requirements = {
        'First Workout': completed_count >= 1,
        'Workout Starter': completed_count >= 5,
        'Fitness Builder': completed_count >= 10,
        'Workout Champion': completed_count >= 25,
        'Consistency Star': streak.current_streak >= 5,
    }

    for achievement_name, requirement_met in achievement_requirements.items():

        if requirement_met:

            achievement = Achievement.objects.filter(
                name=achievement_name,
                is_active=True
            ).first()

            if achievement:
                UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement
                )