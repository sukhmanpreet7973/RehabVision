"""
URL configuration for rehabvision project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'exercises/',
        include('exercises.urls')
    ),

    path(
        'fitness/',
        include('fitness.urls')
    ),

    path(
        'workouts/',
        include('workouts.urls')
    ),

    path(
        'nutrition/',
        include('nutrition.urls')
    ),

    path(
    'progress/',
    include('progress.urls')
    ),

    path(
    'achievements/',
    include('achievements.urls')
    ),

    path(
    'reminders/',
    include('reminders.urls')
    ),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )