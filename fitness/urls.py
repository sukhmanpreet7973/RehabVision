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

    path(
        'assessment/',
        views.fitness_assessment,
        name='fitness_assessment'
    ),

    path(
        'ai-analysis/',
        views.ai_fitness_analysis,
        name='ai_fitness_analysis'
    ),

    path(
    'dashboard/',
    views.fitness_dashboard,
    name='fitness_dashboard'
    ),

]