from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from sqlite3 import IntegrityError

from .models import User
from .forms import User

def dashboard(request):
    """index file for the dashboard, display all user's stats and user settings like pin, email change, password change"""

    pass

def edit(request, field):
    """function to edit the fields/settings for a user"""

    pass

def login(request):

    pass

def logout(request):

    pass

def register(request):

    pass