from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from django.db.utils import IntegrityError

from .models import User
# from .forms import User

def dashboard(request):
    """index file for the dashboard, display all user's stats and user settings like pin, email change, password change"""
    return render(request, 'dashboard/userpage.html')

    pass

def edit(request, field):
    """function to edit the fields/settings for a user"""

    pass

def login_form(request):
    """ logs in a user if correct + message , else sends message in the same form"""
    if request.method == "GET":
        return render(request, 'dashboard/login.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password :
            messages.error(request, f"All fields must be provided", fail_silently=True )
            return render(request, 'dashboard/login.html')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Logged-in", fail_silently=True )
            return HttpResponseRedirect(reverse('vault:index'))
        else:
            messages.error(request, f"Invalid username and/or password", fail_silently=True )
            return render(request, 'dashboard/login.html')


    pass

def logout_user(request):
    logout(request)
    """ logs out current user and redirects to login page"""
    return HttpResponseRedirect(reverse('dashboard:login'))

    pass

def register_form(request):
    """ register a new user"""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # can't be empty field
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # not accepting empty fields
        if not username or not email or not password or not confirmation:
            messages.error(request, "ALL fields must be submitteed", fail_silently=True )

            return render(request, 'dashboard/login.html')
        if password != confirmation:
            messages.error(request, "Passwords MUST match", fail_silently=True )

            return render(request, 'dashboard/login.html')

        try:
            user= User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, f"{username} is already taken", fail_silently=True )
            return render(request, 'dashboard/login.html')

        login(request, user)
        messages.success(request, f"Succesful registration. Welcome {username}", fail_silently=True )

        return HttpResponseRedirect(reverse('vault:index'))
