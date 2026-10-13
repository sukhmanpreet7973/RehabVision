from django.urls import path
from . import views


app_name = 'nutrition'


urlpatterns = [

    path(
        '',
        views.nutrition_dashboard,
        name='nutrition_dashboard'
    ),

    path(
        'generate/',
        views.generate_diet_plan,
        name='generate_diet_plan'
    ),

]