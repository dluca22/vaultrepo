from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib import messages
import json

from .models import Login, History ,Folder
from dashboard.models import User
from .forms import LoginForm, FolderForm


# Create your views here.

@login_required(login_url=reverse_lazy('dashboard:login'), redirect_field_name=None)
def index(request):

    login_form = LoginForm()
    logins = Login.objects.filter(owner=request.user).order_by('title')
    context = {'logins':logins, 'form':login_form}
    return render(request, 'vault/index.html', context=context)

def add_new(request):
    """add <str:type> per aggiungere sia login che note"""
    if request.method == "POST":
        prefix = "https://"
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            uri = login_form.instance.uri
            # if uri was inserted, if add prefix if it is not already presetn
            if uri:
                if not prefix in uri:
                    uri = prefix + uri

            login_form.instance.owner = request.user
            # print(f" dopo : {entry_form.instance}")
            print(f"  : {login_form.cleaned_data}")
            login_form.save()

        return HttpResponseRedirect(reverse('vault:index'))

    else:
        HttpResponseRedirect(reverse('vault:index'))

# or @csrf_protect (cambia behavior on rejection)
@requires_csrf_token
def get_password(request, id):
    """ fare controllo se il login è protected presentare richiesta pin"""
    #LATER  id = int(id, 16)
    # gets the pin from request, if it is not protected, pin is set to false by client.js
    pin = json.loads(request.body)
    user_pin = str(request.user.pin)
    print(type(pin), type(user_pin))

    # try if login is existing
    try:
        login = Login.objects.get(id=id)
    except:
        return JsonResponse({"denied":"Failed request", "message":"This item doesn't exist!"})

    if request.user != login.owner:
        return JsonResponse({"denied":"unauthorized", "message":"You are not the owner"})

    # TODO add decryption

    # if login is protected and pin wasn't provided (may change and just compare if pin is equal to User.pin)
    if login.protected and not pin:
        return JsonResponse({"denied":"unauthorized", "message":"PIN required for this element"})
    elif login.protected and pin != user_pin:
        return JsonResponse({"denied":"unauthorized", "message":"Incorrect PIN"})
    else:

        password = login.password
        return JsonResponse({"success": "successful request", "content": password})


def login_content(request, id):
    """change id to hex"""
    login = Login.objects.get(id=id)
    print(login)
    edit_form = LoginForm(instance=login)
    context = {
        'title': login.title,
        'edit_form':edit_form
    }

    return render(request, 'vault/login_content.html', context=context)

def edit(request, id):
    """edita il field """
    # MAYBE convertire id a hex ??
    pass


def delete(request,id):
    """cancella l'elemento """
    # MAYBE convertire id a hex ??
    pass