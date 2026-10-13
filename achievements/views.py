from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Achievement, UserAchievement, Streak


@login_required
def achievements_dashboard(request):

    # -----------------------------
    # ALL ACTIVE ACHIEVEMENTS
    # -----------------------------

    achievements = Achievement.objects.filter(
        is_active=True
    ).order_by(
        'points',
        'name'
    )

    # -----------------------------
    # USER'S EARNED ACHIEVEMENTS
    # -----------------------------

    earned_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related(
        'achievement'
    ).order_by(
        '-earned_at'
    )

    # -----------------------------
    # USER STREAK
    # -----------------------------

    try:
        streak = request.user.streak

    except Streak.DoesNotExist:

        streak = Streak.objects.create(
            user=request.user
        )

    # -----------------------------
    # TOTAL POINTS
    # -----------------------------

    total_points = sum(
        item.achievement.points
        for item in earned_achievements
    )

    # -----------------------------
    # EARNED ACHIEVEMENT IDs
    # -----------------------------

    earned_ids = set(
        earned_achievements.values_list(
            'achievement_id',
            flat=True
        )
    )

    # -----------------------------
    # SEND DATA TO TEMPLATE
    # -----------------------------

    return render(
        request,
        'achievements/achievements_dashboard.html',
        {
            'achievements': achievements,
            'earned_achievements': earned_achievements,
            'earned_ids': earned_ids,
            'streak': streak,
            'total_points': total_points,
        }
    )