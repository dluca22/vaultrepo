from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from sqlite3 import IntegrityError

from .models import User
# from .forms import User

def dashboard(request):
    """index file for the dashboard, display all user's stats and user settings like pin, email change, password change"""

    pass

def edit(request, field):
    """function to edit the fields/settings for a user"""

    pass

def login_form(request):

    if request.method == "GET":
        return render(request, 'dashboard/login.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
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
    """add logout funct to log user out and reroute to index page """
    return HttpResponseRedirect(reverse('dashboard:login'))

    pass

def register_form(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
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
    pass