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

from .utils import password_generator


# Create your views here.

@login_required(login_url=reverse_lazy('dashboard:login'), redirect_field_name=None)
def index(request):

    folder_query = request.GET.get('folder')
    favorites = request.GET.get('fav')
    search = request.GET.get('q')

    if folder_query:
        if folder_query == "none":
            logins = Login.objects.filter(folder__isnull=True)
        else:
            logins = Login.objects.filter(folder__name=folder_query)
    elif favorites == "true":
        logins = Login.objects.filter(favorite=True)
    elif search:
        logins = Login.objects.filter(title__icontains=search)
    else:
        logins = Login.objects.filter(owner=request.user).order_by('title')



    login_form = LoginForm()
    folder_form = FolderForm()
    folders = (request.user).folders.all()
    context = {'logins':logins,
                'form':login_form,
                 'folder_form': folder_form,
                 'folders': folders}
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
        return HttpResponseRedirect(reverse('vault:index'))

# or @csrf_protect (cambia behavior on rejection)
@requires_csrf_token
def get_password(request, id):
    """ fare controllo se il login è protected presentare richiesta pin"""
    #LATER  id = int(id, 16)
    # gets the pin from request, if it is not protected, pin is set to false by client.js
    pin = json.loads(request.body)
    user_pin = str(request.user.pin)

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
    old_password = login.password

    if request.method == "POST":
        edit_form = LoginForm(request.POST, instance=login)

        if edit_form.is_valid():
            if old_password != edit_form.instance.password and old_password != None:
                History.objects.create(old_passw=old_password, login=login)
            edit_form.save()

            messages.success(request, 'successful edit', fail_silently=True)
            return HttpResponseRedirect(reverse('vault:login_content', args=[id]))

    elif request.method == "GET":
        edit_form = LoginForm(instance=login)

    context = {
        'title': login.title,
        'item_id': id,
        'edit_form':edit_form,
        'history': login.has_history

    }

    return render(request, 'vault/login_content.html', context=context)

def generate_password(request, size):

    passw = password_generator(size)
    print(passw)
    return JsonResponse({"success":'password generated', 'password': passw})



def delete(request,id):
    """cancella l'elemento """
    # MAYBE convertire id a hex ??
    pass


def new_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)

        if form.is_valid():
            form.instance.owner = request.user
            print(form.cleaned_data)
            form.save()

        return HttpResponseRedirect(reverse('vault:index'))

