from django.contrib import admin
from .models import DietPlan, Meal


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'plan_name',
        'goal',
        'daily_calories',
        'protein_grams',
        'carbohydrate_grams',
        'fat_grams',
        'water_liters',
        'is_active',
    )

    search_fields = (
        'user__username',
        'plan_name',
    )

    list_filter = (
        'goal',
        'is_active',
    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'diet_plan',
        'meal_type',
        'meal_name',
        'calories',
        'protein',
        'carbohydrates',
        'fat',
    )

    search_fields = (
        'meal_name',
        'diet_plan__user__username',
    )

    list_filter = ('meal_type',)