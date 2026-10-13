from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import FitnessProfileForm, FitnessGoalForm
from .models import (
    FitnessProfile,
    FitnessGoal,
    FitnessAssessment,
)

@login_required
def fitness_profile(request):

    try:
        profile = request.user.fitness_profile

    except FitnessProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':

        form = FitnessProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            fitness_profile = form.save(
                commit=False
            )

            fitness_profile.user = request.user

            fitness_profile.save()

            return redirect(
                'fitness:fitness_goal'
            )

    else:

        form = FitnessProfileForm(
            instance=profile
        )

    return render(
        request,
        'fitness/fitness_profile.html',
        {
            'form': form
        }
    )

@login_required
def fitness_goal(request):

    try:
        goal = request.user.fitness_goal

    except FitnessGoal.DoesNotExist:
        goal = None

    if request.method == 'POST':

        form = FitnessGoalForm(
            request.POST,
            instance=goal
        )

        if form.is_valid():

            fitness_goal = form.save(
                commit=False
            )

            fitness_goal.user = request.user

            fitness_goal.save()

            return redirect(
                'fitness:fitness_assessment'
            )

    else:

        form = FitnessGoalForm(
            instance=goal
        )

    return render(
        request,
        'fitness/fitness_goal.html',
        {
            'form': form
        }
    )

@login_required
def fitness_assessment(request):

    try:
        profile = request.user.fitness_profile

    except FitnessProfile.DoesNotExist:

        return redirect(
            'fitness:fitness_profile'
        )

    try:
        assessment = request.user.fitness_assessment

    except FitnessAssessment.DoesNotExist:

        assessment = None

    height_m = profile.height / 100

    bmi = profile.weight / (height_m ** 2)

    if profile.gender == 'male':

        bmr = (
            10 * profile.weight
            + 6.25 * profile.height
            - 5 * profile.age
            + 5
        )

    elif profile.gender == 'female':

        bmr = (
            10 * profile.weight
            + 6.25 * profile.height
            - 5 * profile.age
            - 161
        )

    else:


        bmr = (
            10 * profile.weight
            + 6.25 * profile.height
            - 5 * profile.age
            - 78
        )

    activity_multipliers = {

        'sedentary': 1.2,

        'light': 1.375,

        'moderate': 1.55,

        'very_active': 1.725,

        'athlete': 1.9,
    }

    activity_multiplier = activity_multipliers.get(
        profile.activity_level,
        1.2
    )

    daily_calories = bmr * activity_multiplier

    if assessment:

        assessment.bmi = round(
            bmi,
            2
        )

        assessment.bmr = round(
            bmr,
            2
        )

        assessment.daily_calories = round(
            daily_calories,
            2
        )

        assessment.fitness_level = (
            profile.fitness_level
        )

        assessment.save()

    else:

        assessment = FitnessAssessment.objects.create(

            user=request.user,

            bmi=round(
                bmi,
                2
            ),

            bmr=round(
                bmr,
                2
            ),

            daily_calories=round(
                daily_calories,
                2
            ),

            fitness_level=profile.fitness_level,
        )

    return render(
        request,
        'fitness/fitness_assessment.html',
        {
            'assessment': assessment,
            'profile': profile,
        }
    )

@login_required
def ai_fitness_analysis(request):

    try:
        profile = request.user.fitness_profile

    except FitnessProfile.DoesNotExist:

        return redirect(
            'fitness:fitness_profile'
        )

    try:
        goal = request.user.fitness_goal

    except FitnessGoal.DoesNotExist:

        return redirect(
            'fitness:fitness_goal'
        )

    
    try:
        assessment = request.user.fitness_assessment

    except FitnessAssessment.DoesNotExist:

        return redirect(
            'fitness:fitness_assessment'
        )

    analysis = []

    if assessment.bmi < 18.5:

        analysis.append(
            'Your BMI indicates that you are underweight. '
            'A balanced nutrition and strength-focused workout '
            'plan may be beneficial.'
        )

    elif assessment.bmi < 25:

        analysis.append(
            'Your BMI is within the normal range. '
            'You can focus on maintaining your fitness and '
            'achieving your selected fitness goal.'
        )

    elif assessment.bmi < 30:

        analysis.append(
            'Your BMI indicates that you are overweight. '
            'A combination of regular exercise and balanced '
            'nutrition can support your fitness goal.'
        )

    else:

        analysis.append(
            'Your BMI is in the obesity range. '
            'A gradual fitness program and healthy nutrition '
            'can help improve your overall fitness.'
        )

    if profile.fitness_level == 'beginner':

        analysis.append(
            'Since you are a beginner, your workout plan should '
            'start with simple exercises and gradually increase '
            'in intensity.'
        )

    elif profile.fitness_level == 'intermediate':

        analysis.append(
            'Since you have an intermediate fitness level, '
            'your workout can include moderate intensity and '
            'progressive training.'
        )

    else:

        analysis.append(
            'Since you have an advanced fitness level, '
            'your workout can include higher intensity and '
            'progressive resistance training.'
        )

    # --------------------------------------------------------
    # Goal Analysis
    # --------------------------------------------------------

    goal_messages = {

        'weight_loss':
            'Your plan will focus on calorie management, '
            'cardio, and strength training.',

        'muscle_building':
            'Your plan will focus on resistance training, '
            'progressive overload, and adequate nutrition.',

        'strength':
            'Your plan will focus on resistance exercises '
            'and progressive strength development.',

        'endurance':
            'Your plan will focus on cardiovascular training '
            'and gradually improving endurance.',

        'flexibility':
            'Your plan will focus on stretching, mobility, '
            'and flexibility exercises.',

        'general_fitness':
            'Your plan will combine strength, cardio, '
            'mobility, and general fitness exercises.',
    }

    analysis.append(
        goal_messages.get(
            goal.goal,
            'Your workout will be personalized according '
            'to your fitness goal.'
        )
    )

    return render(
        request,
        'fitness/ai_fitness_analysis.html',
        {
            'profile': profile,
            'goal': goal,
            'assessment': assessment,
            'analysis': analysis,
        }
    )

@login_required
def fitness_dashboard(request):

    try:
        profile = request.user.fitness_profile
    except FitnessProfile.DoesNotExist:
        return redirect('fitness:fitness_profile')

    try:
        goal = request.user.fitness_goal
    except FitnessGoal.DoesNotExist:
        return redirect('fitness:fitness_goal')

    try:
        assessment = request.user.fitness_assessment
    except FitnessAssessment.DoesNotExist:
        assessment = None

    from workouts.models import WorkoutPlan, WorkoutSession

    workout_plan = WorkoutPlan.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    today = date.today()

    today_workout = None

    if workout_plan:

        day_number = (
            today - workout_plan.start_date
        ).days + 1

        if day_number > 0:

            today_workout = workout_plan.workout_days.filter(
                day_number=day_number
            ).first()

    completed_workouts = WorkoutSession.objects.filter(
        user=request.user,
        status='completed'
    ).select_related(
        'workout_plan',
        'workout_day'
    ).prefetch_related(
        'exercise_records__exercise'
    ).order_by(
        '-date',
        '-end_time'
    )[:5]

    return render(
        request,
        'fitness/fitness_dashboard.html',
        {
            'profile': profile,
            'goal': goal,
            'assessment': assessment,
            'workout_plan': workout_plan,
            'today_workout': today_workout,
            'completed_workouts': completed_workouts,
        }
    )


@login_required
def landing_page(request):
    return render(
        request,
        'fitness/landing_page.html'
    )
