from django import forms

from .models import Reminder


class ReminderForm(forms.ModelForm):

    class Meta:
        model = Reminder

        fields = [
            'title',
            'description',
            'reminder_type',
            'reminder_time',
            'reminder_date',
            'is_recurring',
            'is_active',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Morning Workout',
                    'class': 'form-control',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Add a short description...',
                    'class': 'form-control',
                    'rows': 3,
                }
            ),

            'reminder_type': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'reminder_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                }
            ),

            'reminder_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'is_recurring': forms.CheckboxInput(
                attrs={
                    'class': 'checkbox',
                }
            ),

            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'checkbox',
                }
            ),
        }