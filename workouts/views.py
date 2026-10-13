from datetime import date
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from exercises.models import Exercise
from fitness.models import FitnessProfile, FitnessGoal
from achievements.services import update_streak_and_achievements
from .models import (
    WorkoutPlan,
    WorkoutDay,
    WorkoutExercise,
    WorkoutSession,
    ExerciseRecord,
)


# --------------------------------------------------
# GENERATE WORKOUT PLAN
# --------------------------------------------------

@login_required
def generate_workout_plan(request):

    try:
        profile = request.user.fitness_profile

    except FitnessProfile.DoesNotExist:
        return redirect('fitness:fitness_profile')

    try:
        goal = request.user.fitness_goal

    except FitnessGoal.DoesNotExist:
        return redirect('fitness:fitness_goal')

    # Deactivate previous active plans

    WorkoutPlan.objects.filter(
        user=request.user,
        is_active=True
    ).update(is_active=False)

    # Create new workout plan

    plan = WorkoutPlan.objects.create(
        user=request.user,
        plan_name=f"{goal.get_goal_display()} Workout Plan",
        goal=goal.goal,
        difficulty=profile.fitness_level,
        duration=profile.workout_duration,
        start_date=date.today(),
        is_active=True
    )

    # --------------------------------------------------
    # NUMBER OF EXERCISES PER DAY
    # --------------------------------------------------

    if profile.workout_duration <= 20:

        exercises_per_day = 3

    elif profile.workout_duration <= 30:

        exercises_per_day = 4

    elif profile.workout_duration <= 45:

        exercises_per_day = 5

    else:

        exercises_per_day = 6

    # --------------------------------------------------
    # EXERCISES GROUPED BY FOCUS
    # --------------------------------------------------

    focus_exercises = {

        'Lower Body': [
            'Bodyweight Squat',
            'Reverse Lunge',
            'Glute Bridge',
            'Calf Raise',
            'Wall Sit',
            'Glute Kickback',
            'Standing Hip Abduction'
        ],

        'Upper Body': [
            'Push Up',
            'Incline Push Up',
            'Wall Push Up',
            'Dumbbell Shoulder Press',
            'Dumbbell Bicep Curl',
            'Dumbbell Row'
        ],

        'Core + Strength': [
            'Plank',
            'Bird Dog',
            'Dead Bug',
            'Bodyweight Squat',
            'Push Up'
        ],

        'Full Body': [
            'Bodyweight Squat',
            'Push Up',
            'Reverse Lunge',
            'Glute Bridge',
            'Dumbbell Row',
            'Plank'
        ],

        'Cardio': [
            'Jumping Jack',
            'Mountain Climber',
            'High Knees'
        ],

        'Cardio + Core': [
            'Jumping Jack',
            'Mountain Climber',
            'High Knees',
            'Plank',
            'Dead Bug'
        ],

        'Lower Body + Cardio': [
            'Bodyweight Squat',
            'Reverse Lunge',
            'Glute Bridge',
            'Jumping Jack',
            'High Knees'
        ],

        'Upper Body + Cardio': [
            'Push Up',
            'Incline Push Up',
            'Wall Push Up',
            'Jumping Jack',
            'Mountain Climber'
        ],

        'Full Body Conditioning': [
            'Bodyweight Squat',
            'Push Up',
            'Mountain Climber',
            'Jumping Jack',
            'Plank'
        ],

        'Lower Body Endurance': [
            'Bodyweight Squat',
            'Reverse Lunge',
            'Glute Bridge',
            'Calf Raise',
            'High Knees'
        ],

        'Upper Body Endurance': [
            'Push Up',
            'Incline Push Up',
            'Wall Push Up',
            'Arm Circles'
        ],

        'Full Body Endurance': [
            'Bodyweight Squat',
            'Push Up',
            'Jumping Jack',
            'Mountain Climber',
            'High Knees'
        ],

        'Lower Body Flexibility': [
            'Hamstring Stretch',
            'Quadriceps Stretch',
            "Child's Pose",
            'Glute Bridge'
        ],

        'Upper Body Mobility': [
            'Arm Circles',
            'Cat Cow',
            "Child's Pose"
        ],

        'Full Body Mobility': [
            'Cat Cow',
            'Arm Circles',
            "Child's Pose",
            'Hamstring Stretch'
        ],

        'Full Body Flexibility': [
            'Hamstring Stretch',
            'Quadriceps Stretch',
            "Child's Pose",
            'Cat Cow'
        ],

        'Core + Mobility': [
            'Bird Dog',
            'Dead Bug',
            'Cat Cow',
            "Child's Pose"
        ],

        'Lower Body Mobility': [
            'Hamstring Stretch',
            'Quadriceps Stretch',
            'Cat Cow',
            "Child's Pose"
        ],

        'Full Body Stretching': [
            'Hamstring Stretch',
            'Quadriceps Stretch',
            "Child's Pose",
            'Cat Cow',
            'Arm Circles'
        ]
    }

    # --------------------------------------------------
    # GOAL BASED WORKOUT DAYS
    # --------------------------------------------------

    goal_days = {

        'muscle_building': [
            'Lower Body',
            'Upper Body',
            'Core + Strength',
            'Full Body',
            'Lower Body',
            'Upper Body',
            'Full Body'
        ],

        'strength': [
            'Lower Body',
            'Upper Body',
            'Core + Strength',
            'Full Body',
            'Lower Body',
            'Upper Body',
            'Full Body'
        ],

        'weight_loss': [
            'Full Body Conditioning',
            'Lower Body + Cardio',
            'Upper Body + Cardio',
            'Cardio + Core',
            'Full Body Conditioning',
            'Cardio',
            'Full Body Conditioning'
        ],

        'endurance': [
            'Cardio',
            'Lower Body Endurance',
            'Upper Body Endurance',
            'Cardio + Core',
            'Full Body Endurance',
            'Cardio',
            'Full Body Endurance'
        ],

        'flexibility': [
            'Full Body Mobility',
            'Lower Body Flexibility',
            'Upper Body Mobility',
            'Core + Mobility',
            'Full Body Flexibility',
            'Lower Body Mobility',
            'Full Body Stretching'
        ],

        'general_fitness': [
            'Full Body',
            'Cardio + Core',
            'Lower Body',
            'Upper Body',
            'Full Body',
            'Cardio + Core',
            'Full Body'
        ]
    }

    selected_days = goal_days.get(
        goal.goal,
        goal_days['general_fitness']
    )

    # --------------------------------------------------
    # NUMBER OF WORKOUT DAYS
    # --------------------------------------------------

    workout_days_count = min(
        profile.workout_days,
        7
    )

    selected_days = selected_days[:workout_days_count]

    selected_days = selected_days.copy()

    if len(selected_days) > 1:
        random.shuffle(selected_days)

    # --------------------------------------------------
    # EQUIPMENT
    # --------------------------------------------------

    available_equipment = (
        profile.equipment_available or ''
    ).lower().strip()

    # --------------------------------------------------
    # FITNESS LEVEL
    # --------------------------------------------------

    level_order = {
        'beginner': 1,
        'intermediate': 2,
        'advanced': 3
    }

    user_level = level_order.get(
        profile.fitness_level,
        1
    )

    # Get all exercises

    all_exercises = list(
        Exercise.objects.all()
    )

    # --------------------------------------------------
    # EQUIPMENT CHECK
    # --------------------------------------------------

    def equipment_is_available(exercise):

        required_equipment = (
            exercise.equipment or 'None'
        ).lower().strip()

        if required_equipment in (
            '',
            'none',
            'bodyweight'
        ):
            return True

        if not available_equipment:
            return False

        return required_equipment in available_equipment

    # --------------------------------------------------
    # FITNESS LEVEL CHECK
    # --------------------------------------------------

    def level_is_suitable(exercise):

        exercise_level = level_order.get(
            exercise.difficulty,
            1
        )

        return exercise_level <= user_level

    # --------------------------------------------------
    # TRACK EXERCISES USED
    # --------------------------------------------------

    used_exercise_ids = set()

    # --------------------------------------------------
    # CREATE EACH WORKOUT DAY
    # --------------------------------------------------

    for day_number, focus in enumerate(
        selected_days,
        start=1
    ):

        day = WorkoutDay.objects.create(
            workout_plan=plan,
            day_number=day_number,
            day_name=f"Day {day_number}",
            focus_area=focus,
            is_rest_day=False
        )

        exercise_names = focus_exercises.get(
            focus,
            []
        )

        valid_exercises = []

        # --------------------------------------------------
        # FIND VALID EXERCISES
        # --------------------------------------------------

        for exercise_name in exercise_names:

            exercise = next(
                (
                    item
                    for item in all_exercises
                    if item.exercise_name == exercise_name
                ),
                None
            )

            if exercise is None:
                continue

            # Equipment check

            if not equipment_is_available(exercise):
                continue

            # Fitness level check

            if not level_is_suitable(exercise):
                continue

            valid_exercises.append(exercise)

        # Randomize exercises

        random.shuffle(valid_exercises)

        # --------------------------------------------------
        # PREFER EXERCISES NOT USED EARLIER
        # --------------------------------------------------

        unused_exercises = [
            exercise
            for exercise in valid_exercises
            if exercise.id not in used_exercise_ids
        ]

        random.shuffle(unused_exercises)

        selected_exercises = unused_exercises[
            :exercises_per_day
        ]

        # --------------------------------------------------
        # ALLOW REPEATED EXERCISES IF NEEDED
        # --------------------------------------------------

        if len(selected_exercises) < exercises_per_day:

            remaining_exercises = [
                exercise
                for exercise in valid_exercises
                if exercise not in selected_exercises
            ]

            random.shuffle(remaining_exercises)

            needed = (
                exercises_per_day
                - len(selected_exercises)
            )

            selected_exercises.extend(
                remaining_exercises[:needed]
            )

        # --------------------------------------------------
        # CREATE WORKOUT EXERCISES
        # --------------------------------------------------

        for order, exercise in enumerate(
            selected_exercises,
            start=1
        ):

            sets = exercise.recommended_sets

            repetitions = (
                exercise.recommended_repetitions
            )

            duration_seconds = (
                exercise.recommended_duration
            )

            rest_seconds = exercise.rest_seconds

            # --------------------------------------------------
            # BEGINNER
            # --------------------------------------------------

            if profile.fitness_level == 'beginner':

                sets = min(
                    sets,
                    3
                )

                if repetitions:

                    repetitions = min(
                        repetitions,
                        12
                    )

            # --------------------------------------------------
            # INTERMEDIATE
            # --------------------------------------------------

            elif profile.fitness_level == 'intermediate':

                sets = min(
                    sets + 1,
                    4
                )

            # --------------------------------------------------
            # ADVANCED
            # --------------------------------------------------

            elif profile.fitness_level == 'advanced':

                sets = min(
                    sets + 1,
                    5
                )

            # --------------------------------------------------
            # SAVE WORKOUT EXERCISE
            # --------------------------------------------------

            WorkoutExercise.objects.create(
                workout_day=day,
                exercise=exercise,
                sets=sets,
                repetitions=repetitions,
                duration_seconds=duration_seconds,
                rest_seconds=rest_seconds,
                order=order,
                notes=(
                    'Maintain proper form and perform '
                    'each movement in a controlled manner.'
                )
            )

            used_exercise_ids.add(
                exercise.id
            )

    # --------------------------------------------------
    # SHOW GENERATED PLAN
    # --------------------------------------------------

    return redirect(
        'workouts:workout_plan',
        plan_id=plan.id
    )


# --------------------------------------------------
# VIEW WORKOUT PLAN
# --------------------------------------------------

@login_required
def workout_plan(request, plan_id):

    plan = WorkoutPlan.objects.filter(
        id=plan_id,
        user=request.user
    ).first()

    if not plan:

        return redirect(
            'workouts:generate_workout_plan'
        )

    return render(
        request,
        'workouts/workout_plan.html',
        {
            'plan': plan
        }
    )


# --------------------------------------------------
# START WORKOUT SESSION
# --------------------------------------------------

@login_required
def start_workout(request, day_id):

    workout_day = WorkoutDay.objects.filter(
        id=day_id,
        workout_plan__user=request.user
    ).first()

    if not workout_day:

        return redirect(
            'fitness:fitness_dashboard'
        )

    # --------------------------------------------------
    # CHECK FOR AN EXISTING ACTIVE SESSION
    # --------------------------------------------------

    existing_session = WorkoutSession.objects.filter(
        user=request.user,
        workout_day=workout_day,
        status='in_progress'
    ).first()

    if existing_session:

        return render(
            request,
            'workouts/workout_session.html',
            {
                'workout_session': existing_session,
                'workout_day': workout_day,
            }
        )

    # --------------------------------------------------
    # CREATE NEW WORKOUT SESSION
    # --------------------------------------------------

    workout_session = WorkoutSession.objects.create(
        user=request.user,
        workout_plan=workout_day.workout_plan,
        workout_day=workout_day,
        date=date.today(),

        # Record exact workout start time
        start_time=timezone.now(),

        status='in_progress'
    )

    return render(
        request,
        'workouts/workout_session.html',
        {
            'workout_session': workout_session,
            'workout_day': workout_day,
        }
    )
@login_required
def complete_workout(request, session_id):

    if request.method != 'POST':
        return redirect('fitness:fitness_dashboard')

    workout_session = WorkoutSession.objects.filter(
        id=session_id,
        user=request.user
    ).first()

    if not workout_session:
        return redirect('fitness:fitness_dashboard')

    # Prevent completing the same workout twice
    if workout_session.status == 'completed':
        return redirect('fitness:fitness_dashboard')

    # Get workout feedback
    difficulty_rating = request.POST.get(
        'difficulty_rating'
    )

    workout_notes = request.POST.get(
        'workout_notes',
        ''
    )

    try:
        difficulty_rating = int(
            difficulty_rating
        )
    except (TypeError, ValueError):
        difficulty_rating = None

    # Make sure the workout has a workout day
    if not workout_session.workout_day:
        return redirect('fitness:fitness_dashboard')

    # ---------------------------------------------
    # RECORD EACH EXERCISE
    # ---------------------------------------------

    total_repetitions = 0
    total_calories = 0

    for workout_exercise in workout_session.workout_day.exercises.all():

        completed = request.POST.get(
            f'completed_{workout_exercise.id}'
        )

        sets_completed = request.POST.get(
            f'sets_{workout_exercise.id}',
            0
        )

        repetitions_completed = request.POST.get(
            f'reps_{workout_exercise.id}',
            0
        )

        notes = request.POST.get(
            f'notes_{workout_exercise.id}',
            ''
        )

        try:
            sets_completed = int(
                sets_completed
            )
        except (TypeError, ValueError):
            sets_completed = 0

        try:
            repetitions_completed = int(
                repetitions_completed
            )
        except (TypeError, ValueError):
            repetitions_completed = 0

        # If exercise was not completed
        if not completed:
            sets_completed = 0
            repetitions_completed = 0

        # ---------------------------------------------
        # CALCULATE EXERCISE CALORIES
        # ---------------------------------------------

        exercise_calories = (
            sets_completed
            * repetitions_completed
            * 0.25
        )

        # ---------------------------------------------
        # SAVE EXERCISE RECORD
        # ---------------------------------------------

        ExerciseRecord.objects.update_or_create(
            workout_session=workout_session,
            exercise=workout_exercise.exercise,
            defaults={
                'sets_completed': sets_completed,
                'repetitions_completed': repetitions_completed,
                'duration_seconds': 0,
                'calories_burned': round(
                    exercise_calories,
                    2
                ),
                'notes': notes,
            }
        )

        total_repetitions += (
            sets_completed
            * repetitions_completed
        )

        total_calories += exercise_calories

    # ---------------------------------------------
    # RECORD END TIME
    # ---------------------------------------------

    workout_session.status = 'completed'

    workout_session.end_time = timezone.now()

    # ---------------------------------------------
    # SAVE RATING
    # ---------------------------------------------

    workout_session.difficulty_rating = (
        difficulty_rating
    )

    # ---------------------------------------------
    # SAVE NOTES
    # ---------------------------------------------

    workout_session.notes = workout_notes

    # ---------------------------------------------
    # CALCULATE DURATION
    # ---------------------------------------------

    if workout_session.start_time:

        duration = (
            workout_session.end_time
            - workout_session.start_time
        )

        workout_session.duration_minutes = max(
            1,
            round(
                duration.total_seconds() / 60
            )
        )

    # ---------------------------------------------
    # SAVE TOTAL CALORIES
    # ---------------------------------------------

    workout_session.calories_burned = round(
        total_calories,
        2
    )

    # ---------------------------------------------
    # SAVE WORKOUT SESSION
    # ---------------------------------------------

    workout_session.save()

    # ---------------------------------------------
    # UPDATE STREAK & ACHIEVEMENTS
    # ---------------------------------------------

    update_streak_and_achievements(
        request.user
    )

    # ---------------------------------------------
    # RETURN TO DASHBOARD
    # ---------------------------------------------

    return redirect(
        'fitness:fitness_dashboard'
    )
@login_required
def workout_history(request):

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
    )

    return render(
        request,
        'workouts/workout_history.html',
        {
            'completed_workouts': completed_workouts,
        }
    )    