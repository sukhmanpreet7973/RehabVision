
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

      
        if password != confirm_password:

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Passwords do not match.'
                }
            )

      
        if User.objects.filter(username=username).exists():

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Username already exists.'
                }
            )

        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        
        return redirect('accounts:login')

    return render(
        request,
        'accounts/register.html'
    )

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

     
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            
            login(request, user)

           
            from fitness.models import FitnessProfile, FitnessGoal

           
            if not FitnessProfile.objects.filter(user=user).exists():

                return redirect('fitness:fitness_profile')

            
            if not FitnessGoal.objects.filter(user=user).exists():

                return redirect('fitness:fitness_goal')

           
            return redirect('fitness:landing_page')

        
        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'accounts/login.html'
    )

def logout_view(request):

    logout(request)

    return redirect('accounts:login')
