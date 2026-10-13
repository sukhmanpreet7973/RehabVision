from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import WeightRecord, ProgressRecord
from workouts.models import WorkoutSession


@login_required
def progress_dashboard(request):

    # -----------------------------
    # WEIGHT RECORDS
    # -----------------------------

    weight_records = WeightRecord.objects.filter(
        user=request.user
    ).order_by('-recorded_date')

    latest_weight = weight_records.first()

    weight_change = 0

    if weight_records.count() >= 2:

        latest = weight_records[0]
        previous = weight_records[1]

        weight_change = round(
            latest.weight - previous.weight,
            1
        )

    # -----------------------------
    # COMPLETED WORKOUTS
    # -----------------------------

    completed_workouts = WorkoutSession.objects.filter(
        user=request.user,
        status='completed'
    ).prefetch_related(
        'exercise_records'
    )

    total_workouts = completed_workouts.count()

    total_minutes = sum(
        workout.duration_minutes
        for workout in completed_workouts
    )

    total_calories = sum(
        workout.calories_burned
        for workout in completed_workouts
    )

    # -----------------------------
    # EXERCISE STATISTICS
    # -----------------------------

    total_repetitions = 0

    performance_scores = []

    for workout in completed_workouts:

        for record in workout.exercise_records.all():

            total_repetitions += record.repetitions_completed

            if record.performance_score is not None:
                performance_scores.append(
                    record.performance_score
                )

    # -----------------------------
    # AVERAGE PERFORMANCE
    # -----------------------------

    if performance_scores:

        average_performance = round(
            sum(performance_scores)
            / len(performance_scores),
            1
        )

    else:

        average_performance = 0

    # -----------------------------
    # GOAL COMPLETION
    # -----------------------------

    try:

        fitness_goal = request.user.fitness_goal

        goal_completion = 0

        if fitness_goal:

            # Basic progress calculation.
            # 20 completed workouts = 100%

            goal_completion = min(
                round(
                    (total_workouts / 20) * 100
                ),
                100
            )

    except Exception:

        goal_completion = 0

    # -----------------------------
    # CREATE / UPDATE PROGRESS RECORD
    # -----------------------------

    progress_record = ProgressRecord.objects.update_or_create(

        user=request.user,

        date=__import__('datetime').date.today(),

        defaults={

            'workouts_completed':
                total_workouts,

            'total_workout_minutes':
                total_minutes,

            'calories_burned':
                total_calories,

            'total_repetitions':
                total_repetitions,

            'average_performance_score':
                average_performance,

            'goal_completion_percentage':
                goal_completion,
        }
    )[0]

    # -----------------------------
    # SEND DATA TO TEMPLATE
    # -----------------------------

    return render(

        request,

        'progress/progress_dashboard.html',

        {

            'weight_records':
                weight_records,

            'latest_weight':
                latest_weight,

            'weight_change':
                weight_change,

            'total_workouts':
                total_workouts,

            'total_minutes':
                total_minutes,

            'total_calories':
                total_calories,

            'total_repetitions':
                total_repetitions,

            'average_performance':
                average_performance,

            'goal_completion':
                goal_completion,

            'progress_record':
                progress_record,
        }
    )