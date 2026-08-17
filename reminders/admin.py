from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'reminder_type',
        'reminder_time',
        'reminder_date',
        'is_recurring',
        'is_active',
    )

    search_fields = (
        'user__username',
        'title',
    )

    list_filter = (
        'reminder_type',
        'is_recurring',
        'is_active',
    )