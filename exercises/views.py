from django.shortcuts import render, get_object_or_404
from .models import Exercise


def exercise_list(request):
    exercises = Exercise.objects.all()

    return render(
        request,
        'exercises/exercise_list.html',
        {
            'exercises': exercises
        }
    )


def exercise_detail(request, pk):
    exercise = get_object_or_404(
        Exercise,
        pk=pk
    )

    return render(
        request,
        'exercises/exercise_detail.html',
        {
            'exercise': exercise
        }
    )