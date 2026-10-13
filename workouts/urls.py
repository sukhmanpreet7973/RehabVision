from django.urls import path

from . import views

app_name = 'workouts'

urlpatterns = [

    path(
        'generate/',
        views.generate_workout_plan,
        name='generate_workout_plan'
    ),

    path(
        'plan/<int:plan_id>/',
        views.workout_plan,
        name='workout_plan'
    ),

    path(
        'start/<int:day_id>/',
        views.start_workout,
        name='start_workout'
    ),

    path(
        'complete/<int:session_id>/',
        views.complete_workout,
        name='complete_workout'
    ),

    path(
    'history/', 
    views.workout_history, 
    name='workout_history'
    ),

]