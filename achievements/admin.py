from django.contrib import admin
from .models import Achievement, UserAchievement, Streak


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'points',
        'is_active',
        'created_at',
    )

    search_fields = (
        'name',
        'description',
    )

    list_filter = ('is_active',)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'achievement',
        'earned_at',
    )

    search_fields = (
        'user__username',
        'achievement__name',
    )


@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'current_streak',
        'longest_streak',
        'last_workout_date',
        'updated_at',
    )

    search_fields = ('user__username',)