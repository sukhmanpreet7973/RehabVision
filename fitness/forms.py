from django import forms

from .models import (
    FitnessProfile,
    FitnessGoal,
    FitnessAssessment,
)


# ============================================================
# FITNESS PROFILE FORM
# ============================================================

class FitnessProfileForm(forms.ModelForm):

    class Meta:

        model = FitnessProfile

        fields = [
            'age',
            'gender',
            'height',
            'weight',
            'fitness_level',
            'activity_level',
            'equipment_available',
            'workout_duration',
            'workout_days',
        ]

        widgets = {

            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your age',
                    'min': 13,
                    'max': 100,
                }
            ),

            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'height': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Height in cm',
                    'step': '0.1',
                }
            ),

            'weight': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Weight in kg',
                    'step': '0.1',
                }
            ),

            'fitness_level': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'activity_level': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'equipment_available': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: Dumbbells, Resistance Bands, None'
                    ),
                    'rows': 3,
                }
            ),

            'workout_duration': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Minutes per workout',
                    'min': 10,
                    'max': 180,
                }
            ),

            'workout_days': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Days per week',
                    'min': 1,
                    'max': 7,
                }
            ),
        }

        labels = {

            'age': 'Age',

            'gender': 'Gender',

            'height': 'Height (cm)',

            'weight': 'Weight (kg)',

            'fitness_level': 'Fitness Level',

            'activity_level': 'Activity Level',

            'equipment_available': 'Available Equipment',

            'workout_duration': 'Workout Duration (minutes)',

            'workout_days': 'Workout Days per Week',
        }


# ============================================================
# FITNESS GOAL FORM
# ============================================================

class FitnessGoalForm(forms.ModelForm):

    class Meta:

        model = FitnessGoal

        fields = [
            'goal',
            'target_weight',
            'target_date',
        ]

        widgets = {

            'goal': forms.RadioSelect(),

            'target_weight': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter target weight in kg',
                    'step': '0.1',
                    'min': 20,
                    'max': 300,
                }
            ),

            'target_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
        }

        labels = {

            'goal': 'Fitness Goal',

            'target_weight': 'Target Weight (kg)',

            'target_date': 'Target Date',
        }

    def clean_target_weight(self):

        target_weight = self.cleaned_data.get(
            'target_weight'
        )

        if target_weight is not None and target_weight <= 0:

            raise forms.ValidationError(
                'Target weight must be greater than 0.'
            )

        return target_weight


 # ============================================================
# FITNESS ASSESSMENT FORM
# ============================================================

class FitnessAssessmentForm(forms.ModelForm):

    class Meta:

        model = FitnessAssessment

        fields = [
            'bmi',
            'bmr',
            'daily_calories',
            'fitness_level',
        ]

        widgets = {

            'bmi': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                }
            ),

            'bmr': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                }
            ),

            'daily_calories': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                }
            ),

            'fitness_level': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                }
            ),
        }

        labels = {

            'bmi': 'BMI',

            'bmr': 'BMR (Calories/Day)',

            'daily_calories': 'Daily Calorie Requirement',

            'fitness_level': 'Fitness Level',
        }   