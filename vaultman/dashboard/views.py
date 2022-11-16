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

def login(request):

    if request.method == "GET":
        return render(request, 'dashboard/login.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('vault:index'))
        else:
            return render(request, 'vault/login.html', {"message": "Invalid username and/or password."})


    pass

def logout(request):

    pass

def register(request):

    pass