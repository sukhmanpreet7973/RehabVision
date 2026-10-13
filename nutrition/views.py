from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import DietPlan, Meal


@login_required
def nutrition_dashboard(request):

    diet_plan = DietPlan.objects.filter(
        user=request.user,
        is_active=True
    ).prefetch_related(
        'meals'
    ).first()

    return render(
        request,
        'nutrition/nutrition_dashboard.html',
        {
            'diet_plan': diet_plan,
        }
    )


@login_required
def generate_diet_plan(request):

    if request.method != 'POST':
        return redirect('nutrition:nutrition_dashboard')

    try:
        goal = request.user.fitness_goal
        assessment = request.user.fitness_assessment
    except Exception:
        return redirect('fitness:fitness_dashboard')

    # -----------------------------
    # CALORIE CALCULATION
    # -----------------------------

    calories = assessment.daily_calories

    if goal.goal == 'weight_loss':
        calories = calories - 300

    elif goal.goal == 'muscle_building':
        calories = calories + 300

    calories = max(1200, calories)

    # -----------------------------
    # MACRONUTRIENTS
    # -----------------------------

    protein = round(
        (calories * 0.30) / 4
    )

    carbohydrates = round(
        (calories * 0.40) / 4
    )

    fat = round(
        (calories * 0.30) / 9
    )

    # -----------------------------
    # DEACTIVATE OLD PLAN
    # -----------------------------

    DietPlan.objects.filter(
        user=request.user,
        is_active=True
    ).update(
        is_active=False
    )

    # -----------------------------
    # CREATE NEW DIET PLAN
    # -----------------------------

    diet_plan = DietPlan.objects.create(
        user=request.user,
        plan_name='Personalized Nutrition Plan',
        goal=goal.goal,
        daily_calories=round(calories),
        protein_grams=protein,
        carbohydrate_grams=carbohydrates,
        fat_grams=fat,
        water_liters=2.5,
        start_date=date.today(),
        is_active=True
    )

    # -----------------------------
    # GOAL-BASED MEALS
    # -----------------------------

    if goal.goal == 'weight_loss':

        meals = [

            {
                'meal_type': 'breakfast',
                'meal_name': 'Oats & Fruit Breakfast',
                'description': (
                    'Oats with low-fat milk or curd, '
                    'fresh fruit and a small portion of nuts.'
                ),
                'serving_size': '1 bowl'
            },

            {
                'meal_type': 'lunch',
                'meal_name': 'Dal, Roti & Vegetable Lunch',
                'description': (
                    'Dal with whole-wheat roti, mixed vegetables '
                    'and a bowl of curd.'
                ),
                'serving_size': '2 roti + 1 bowl dal + vegetables'
            },

            {
                'meal_type': 'snack',
                'meal_name': 'Fruit & Nuts',
                'description': (
                    'One seasonal fruit with a small handful '
                    'of almonds or walnuts.'
                ),
                'serving_size': '1 fruit + small handful of nuts'
            },

            {
                'meal_type': 'dinner',
                'meal_name': 'Paneer & Vegetable Dinner',
                'description': (
                    'Light paneer with cooked vegetables '
                    'and whole-wheat roti.'
                ),
                'serving_size': '1 bowl + 1–2 roti'
            }

        ]

    elif goal.goal == 'muscle_building':

        meals = [

            {
                'meal_type': 'breakfast',
                'meal_name': 'High-Protein Breakfast',
                'description': (
                    'Oats with milk, banana, peanut butter '
                    'and eggs or paneer.'
                ),
                'serving_size': '1 large bowl + protein source'
            },

            {
                'meal_type': 'lunch',
                'meal_name': 'Protein-Rich Lunch',
                'description': (
                    'Rice or roti with dal, paneer or chicken, '
                    'vegetables and curd.'
                ),
                'serving_size': '2–3 roti or 1 bowl rice + protein'
            },

            {
                'meal_type': 'snack',
                'meal_name': 'Protein Snack',
                'description': (
                    'Greek yogurt or milk with banana, '
                    'nuts and peanut butter.'
                ),
                'serving_size': '1 bowl'
            },

            {
                'meal_type': 'dinner',
                'meal_name': 'High-Protein Dinner',
                'description': (
                    'Paneer, chicken or dal with rice/roti '
                    'and vegetables.'
                ),
                'serving_size': '1 protein serving + 2 roti'
            }

        ]

    elif goal.goal == 'maintenance':

        meals = [

            {
                'meal_type': 'breakfast',
                'meal_name': 'Balanced Breakfast',
                'description': (
                    'Oats or whole-grain toast with milk, '
                    'fruit and eggs or paneer.'
                ),
                'serving_size': '1 balanced serving'
            },

            {
                'meal_type': 'lunch',
                'meal_name': 'Balanced Indian Lunch',
                'description': (
                    'Roti or rice with dal, vegetables, '
                    'protein and curd.'
                ),
                'serving_size': 'Balanced plate'
            },

            {
                'meal_type': 'snack',
                'meal_name': 'Fruit & Yogurt',
                'description': (
                    'Seasonal fruit with plain yogurt '
                    'and a few nuts.'
                ),
                'serving_size': '1 bowl'
            },

            {
                'meal_type': 'dinner',
                'meal_name': 'Balanced Dinner',
                'description': (
                    'Roti or rice with dal or paneer, '
                    'vegetables and salad.'
                ),
                'serving_size': 'Balanced plate'
            }

        ]

    else:

        meals = [

            {
                'meal_type': 'breakfast',
                'meal_name': 'Healthy Breakfast',
                'description': (
                    'Oats or whole-grain breakfast with '
                    'milk, fruit and protein.'
                ),
                'serving_size': '1 bowl'
            },

            {
                'meal_type': 'lunch',
                'meal_name': 'Healthy Indian Lunch',
                'description': (
                    'Roti or rice with dal, vegetables, '
                    'protein and curd.'
                ),
                'serving_size': 'Balanced plate'
            },

            {
                'meal_type': 'snack',
                'meal_name': 'Healthy Snack',
                'description': (
                    'Fresh fruit, yogurt or a small serving '
                    'of nuts.'
                ),
                'serving_size': '1 serving'
            },

            {
                'meal_type': 'dinner',
                'meal_name': 'Healthy Dinner',
                'description': (
                    'Protein source with vegetables '
                    'and roti or rice.'
                ),
                'serving_size': 'Balanced plate'
            }

        ]

    # -----------------------------
    # CREATE MEALS
    # -----------------------------

    meal_percentages = {
        'breakfast': 0.25,
        'lunch': 0.30,
        'snack': 0.15,
        'dinner': 0.30,
    }

    for meal in meals:

        percentage = meal_percentages[
            meal['meal_type']
        ]

        Meal.objects.create(
            diet_plan=diet_plan,
            meal_type=meal['meal_type'],
            meal_name=meal['meal_name'],
            description=meal['description'],
            calories=round(
                calories * percentage
            ),
            protein=round(
                protein * percentage
            ),
            carbohydrates=round(
                carbohydrates * percentage
            ),
            fat=round(
                fat * percentage
            ),
            serving_size=meal['serving_size'],
        )

    return redirect(
        'nutrition:nutrition_dashboard'
    )