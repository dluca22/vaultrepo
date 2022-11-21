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

def edit_pin(request):
    if request.method == "POST":

        user = request.user
        master_password = request.POST['master_password']
        old_pin = request.POST['old_pin']
        new_pin = request.POST['new_pin']
        confirmation = request.POST['confirm_pin']


        # if check password failed (using hashed check comparison)
        if not user.check_password(master_password):
            messages.error(request, 'Master Password was incorrect',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        # if the user user PIN check fails TODO add hashing to this too
        elif old_pin != user.pin:
            messages.error(request, 'Current PIN was incorrect',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))

        # if pin and confirmation don't match, or pin is more than 4 digits
        elif new_pin != confirmation or len(new_pin) > 4:
            messages.error(request, 'New PIN check failed',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        # if new PIN is the same as old PIN
        elif new_pin == old_pin:
            messages.warning(request, 'PIN not updated: it was the same as the current one',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))

        # if clears all confitions
        else:
            print("success")
            user.pin = new_pin
            user.save()
            messages.success(request, 'PIN updated',fail_silently=True)

            return HttpResponseRedirect(reverse('dashboard:dashboard'))

def set_pin(request):
    if request.method == "POST":

        user = request.user
        new_pin = request.POST['new_pin']

        if len(new_pin) > 4:
            messages.error(request, 'PIN must be 4 digit only',fail_silently=True)

            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        user.pin = new_pin
        user.save()

        messages.success(request, 'PIN set',fail_silently=True)
        return HttpResponseRedirect(reverse('dashboard:dasPINNhboard'))