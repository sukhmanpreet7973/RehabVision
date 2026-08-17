from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import FitnessProfileForm, FitnessGoalForm
from .models import FitnessProfile, FitnessGoal


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

            # We will connect this to the
            # assessment page next.
            return redirect(
                'fitness:fitness_goal'
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