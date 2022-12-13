from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from django.db.utils import IntegrityError

from vault.encrypt_util import encrypt, decrypt

from .models import User
# from .forms import User

@login_required(login_url=reverse_lazy('dashboard:login'), redirect_field_name=None)
def dashboard(request):
    """index file for the dashboard, display all user's stats and user settings like pin, email change, password change"""

    folders = request.user.folders.all()
    context = {'folders': folders}
    return render(request, 'dashboard/userpage.html', context=context)

    pass

# ===================================================

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


# ===================================================

def logout_user(request):
    logout(request)
    """ logs out current user and redirects to login page"""
    return HttpResponseRedirect(reverse('dashboard:login'))


# ===================================================

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


# ===================================================

def edit_pin(request):
    if request.method == "POST":

        user = request.user
        # pw, old pin, new pin and confirmation derived from the form
        master_password = request.POST['master_password']
        old_pin = request.POST['old_pin']
        new_pin = request.POST['new_pin']
        confirmation = request.POST['confirm_pin']


        # if check password failed (using hashed check comparison)
        if not user.check_password(master_password):
            messages.error(request, 'Master Password was incorrect',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))

        # if form old_pin as cleartext IS NOT decrypted(user.pin)
        elif old_pin != decrypt(user.pin):
            messages.error(request, 'Current PIN was incorrect',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))

        # if pin and confirmation don't match, or pin is not 4 digits
        elif new_pin != confirmation or len(new_pin) != 4:
            messages.error(request, 'New PIN check failed',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        # if new PIN is the same as old PIN
        elif new_pin == old_pin:
            messages.warning(request, 'PIN not updated: it was the same as the current one',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))

        # if clears all conditions, encrypt pin and save
        else:
            user.pin = encrypt(new_pin)
            user.save()
            messages.success(request, 'PIN updated',fail_silently=True)

            return HttpResponseRedirect(reverse('dashboard:dashboard'))


# ===================================================

def set_pin(request):
    if request.method == "POST":

        user = request.user
        new_pin = request.POST['new_pin']

        if len(new_pin) != 4:
            messages.error(request, 'PIN must be 4 digits',fail_silently=True)

            return HttpResponseRedirect(reverse('dashboard:dashboard'))

        user.pin = encrypt(new_pin)
        user.save()

        messages.success(request, 'PIN set',fail_silently=True)
        return HttpResponseRedirect(reverse('dashboard:dashboard'))


# ===================================================

def change_masterpassword(request):
    if request.method == "POST":
        user = request.user
        email = request.POST['email']
        current_password = request.POST['current_password']
        pin = request.POST['pin']

        new_password = request.POST['new_password']
        confirmation = request.POST['confirmation']

        if new_password != confirmation:
            messages.error(request, "Passwords do not match",fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))


        email_check = email == user.email
        pin_check = pin == user.get_pin
        pw_check = user.check_password(current_password)

        if email_check and pin_check and pw_check:
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password updated!',fail_silently=True)
            messages.success(request, 'Log back in',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:login'))

        else:
            messages.error(request, 'Form check failed',fail_silently=True)
            messages.error(request, 'Password unchanged',fail_silently=True)

            return HttpResponseRedirect(reverse('dashboard:logout'))



# ===================================================

def change_email(request):
    if request.method == "POST":
        user = request.user
        new_email = request.POST['email']
        password = request.POST['password']


        if user.check_password(password) :
            user.email = new_email
            user.save()
            messages.success(request, 'Email updated',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
            messages.error(request, 'Failed check',fail_silently=True)
            messages.error(request, 'Email unchanged',fail_silently=True)
            return HttpResponseRedirect(reverse('dashboard:dashboard'))


# ===================================================


def delete_account(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # matching fields to get bool values
        username_match = username == request.user.username
        email_match = email== request.user.email
        pw_match = request.user.check_password(password)

        # if all 3 bool values are true, process delete()
        if username_match and email_match and pw_match:
            request.user.delete()
            messages.success(request, "Account deleted.")
            return HttpResponseRedirect(reverse('dashboard:login'))

        messages.error(request, "Not deleted.")
        messages.error(request, "Form did not match.")
        return HttpResponseRedirect(reverse('dashboard:dashboard'))