from django.urls import path
from . import views


app_name = 'fitness'


urlpatterns = [

    path(
        'profile/',
        views.fitness_profile,
        name='fitness_profile'
    ),

    path(
        'goal/',
        views.fitness_goal,
        name='fitness_goal'
    ),

]