from django.urls import path
from . import views


app_name = 'reminders'


urlpatterns = [

    path(
        '',
        views.reminder_dashboard,
        name='reminder_dashboard'
    ),

    path(
        'create/',
        views.create_reminder,
        name='create_reminder'
    ),

    path(
        'edit/<int:reminder_id>/',
        views.edit_reminder,
        name='edit_reminder'
    ),

    path(
        'delete/<int:reminder_id>/',
        views.delete_reminder,
        name='delete_reminder'
    ),

]