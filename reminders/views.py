from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Reminder
from .forms import ReminderForm


@login_required
def reminder_dashboard(request):

    reminders = Reminder.objects.filter(
        user=request.user
    ).order_by(
        'reminder_time'
    )

    active_reminders = reminders.filter(
        is_active=True
    )

    return render(
        request,
        'reminders/reminder_dashboard.html',
        {
            'reminders': reminders,
            'active_reminders': active_reminders,
        }
    )


@login_required
def create_reminder(request):

    if request.method == 'POST':

        form = ReminderForm(request.POST)

        if form.is_valid():

            reminder = form.save(commit=False)

            reminder.user = request.user

            reminder.save()

            return redirect(
                'reminders:reminder_dashboard'
            )

    else:

        form = ReminderForm()

    return render(
        request,
        'reminders/create_reminder.html',
        {
            'form': form,
        }
    )

@login_required
def edit_reminder(request, reminder_id):

    reminder = Reminder.objects.filter(
        id=reminder_id,
        user=request.user
    ).first()

    if not reminder:
        return redirect(
            'reminders:reminder_dashboard'
        )

    if request.method == 'POST':

        form = ReminderForm(
            request.POST,
            instance=reminder
        )

        if form.is_valid():

            form.save()

            return redirect(
                'reminders:reminder_dashboard'
            )

    else:

        form = ReminderForm(
            instance=reminder
        )

    return render(
        request,
        'reminders/create_reminder.html',
        {
            'form': form,
            'editing': True,
        }
    )


@login_required
def delete_reminder(request, reminder_id):

    reminder = Reminder.objects.filter(
        id=reminder_id,
        user=request.user
    ).first()

    if not reminder:
        return redirect(
            'reminders:reminder_dashboard'
        )

    if request.method == 'POST':

        reminder.delete()

        return redirect(
            'reminders:reminder_dashboard'
        )

    return render(
        request,
        'reminders/delete_reminder.html',
        {
            'reminder': reminder,
        }
    )    