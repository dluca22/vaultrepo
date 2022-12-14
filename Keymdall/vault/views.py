from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models.functions import Lower

from django.contrib import messages
import json

from .models import Login, History ,Folder
from dashboard.models import User
from .forms import LoginForm, FolderForm

from .utils import password_generator, format_uri
from .encrypt_util import encrypt, decrypt


# ===================================================

@login_required(login_url=reverse_lazy('dashboard:login'), redirect_field_name=None)
def index(request):

    # if there is a query for each of these fields
    folder_query = request.GET.get('folder')
    filter = request.GET.get('filter')
    search = request.GET.get('q')

    if folder_query:
        # if query is from btn "none" category, selects only items not in folder
        if folder_query == "none":
            logins = Login.objects.filter(folder__isnull=True, owner=request.user)
        # else, filter where folder name is the one in the query
        else:
            logins = Login.objects.filter(folder__name=folder_query, owner=request.user)
    # if query is for fav items, selects only those
    elif filter == "fav":
        logins = Login.objects.filter(owner=request.user, favorite=True)
    elif filter == "logins":
        logins = Login.objects.filter(favorite=True, owner=request.user)
    # elif filter == "notes":
    #     logins = Note.objects.filter(owner=request.user).order_by('title')
    # if the query is a ?q search request, selects ones where the title contains the word in search (insensitive contains)
    elif search:
        logins = Login.objects.filter(title__icontains=search, owner=request.user)
    # else selects all logins
    else:
        logins = Login.objects.filter(owner=request.user).order_by('title')


    # builds forms and folder qset and adds to the context
    login_form = LoginForm(user=request.user)
    folder_form = FolderForm()
    folders = (request.user).folders.all().order_by(Lower('name'))
    context = {  'logins':logins,
                 'form':login_form,
                 'folder_form': folder_form,
                 'folders': folders}
                #  return index page with context
    return render(request, 'vault/index.html', context=context)


# ===================================================


def add_new(request):
    """add <str:type> per aggiungere sia login che note"""
    if request.method == "POST":

        login_form = LoginForm(request.POST, user=request.user)

        if login_form.is_valid():
            # get uri field from form
            uri = format_uri(login_form.instance.uri)
            login_form.instance.uri = encrypt(uri)


            # encrypt also password and note then save
            # if field is "None", encrypt empty space ""
            passw = login_form.instance.password
            note = login_form.instance.note
            login_form.instance.password = encrypt(login_form.instance.password)
            login_form.instance.note = encrypt(login_form.instance.note)

            login_form.instance.owner = request.user
            login_form.save()
            # send message then redirect to index
            messages.success(request, "New element created!")
        return HttpResponseRedirect(reverse('vault:index'))

    else:
        return HttpResponseRedirect(reverse('vault:index'))

# ===================================================

# or @csrf_protect (cambia behavior on rejection)
@requires_csrf_token
def get_password(request, id):
    """ fare controllo se il login ?? protected presentare richiesta pin"""
    #LATER  id = int(id, 16)
    # gets the pin from request, if it is not protected, pin is set to false by client.js
    pin = json.loads(request.body)
    # TODO convert to @property so that it can be decrypted from models.py
    user_pin = decrypt(request.user.pin)
    # try if login is existing
    try:
        login = Login.objects.get(id=id)
    except:
        return JsonResponse({"denied":"Failed request", "message":"This item does not exist!"})

    if request.user != login.owner:
        return JsonResponse({"denied":"unauthorized", "message":"You are not the owner"})



    # if login is protected and pin wasn't provided (may change and just compare if pin is equal to User.pin)
    if login.protected and not pin:
        return JsonResponse({"denied":"unauthorized", "message":"Item locked! PIN is required"})

    elif login.protected and pin != user_pin:
        return JsonResponse({"denied":"unauthorized", "message":"Incorrect PIN"})
    else:

        password = decrypt(login.password)
        return JsonResponse({"success": "successful request", "content": password})

# ===================================================

@requires_csrf_token
def login_content(request, id):
    """GET request shows the Item content in a form, POST request edits the element
    both check wether the Item exists and the user is the owner
    """
    # TODO change id to hex

    try:
        login = Login.objects.get(id=id, owner=request.user)
    except:
        messages.error(request, "Unauthorized: You are not the owner", fail_silently=True)
        return HttpResponseRedirect(reverse('vault:index'))

    if request.method == "GET":
        # decrypt the fields before running instances of login (uses _meta attribute to compile form)
        # login = login.decrypted (this property does not work, does not return a model instance but a dictionary)
        login.password = decrypt(login.password)
        login.uri = decrypt(login.uri)
        login.note = decrypt(login.note)

        # 'user' **kwargs is used to return the folder instance beloging to the user
        edit_form = LoginForm(instance=login, user=request.user)

        context = {
            'title': login.title,
            'item_id': id,
            'form':edit_form,
            'history': [decrypt(str(old_pw)) for old_pw in login.passw_history]

        }
        return render(request, 'vault/login_content.html', context=context)

    # decrypt old password to compare for changes

    elif request.method == "POST":
        """ edit request, if password changed, stores the old password in History table """
        old_password = login.password
        old_password_clear = decrypt(old_password)
        edit_form = LoginForm(request.POST, instance=login, user=request.user)

        if edit_form.is_valid():

            # Check if new password is different from old password, and is NOT null, then stores old_passw in History table

            new_pw = edit_form.instance.password
            #
            if old_password_clear != new_pw and old_password_clear != "" :
                # if cleartext old password is not equal to the new password, store login.password(not decrypted) in the history model
                History.objects.create(old_passw=old_password, login=login)

            edit_form.instance.password = encrypt(edit_form.instance.password)
            uri = format_uri(edit_form.instance.uri)
            edit_form.instance.uri = encrypt(uri)
            edit_form.instance.note = encrypt(edit_form.instance.note)
            edit_form.save()

            messages.success(request, 'Successful edit', fail_silently=True)
            return HttpResponseRedirect(reverse('vault:login_content', args=[id]))
        # if messages not valid
        else:
            messages.error(request, 'Invalid form', fail_silently=True)
            return HttpResponseRedirect(reverse('vault:login_content', args=[id]))


# ===================================================


def generate_password(request, size):
    try:
        passw = password_generator(size)
        return JsonResponse({"success":"successful request", "message":'Password generated!', 'password': passw})
    except:
        return JsonResponse({"denied": "error", "message": 'An unexpected error occurred'})

# ===================================================

@requires_csrf_token
def delete(request,id):
    """cancella l'elemento """
    if request.method == "DELETE":
        try:
            login = Login.objects.get(id=id)
        except:
            return JsonResponse({"denied":'Failed request', "message":"This item does not exist!"})


        if login.owner == request.user:
            login.delete()
            return JsonResponse({"success":"Successful requesta", "message" : 'deleted successfully'})
        else:
            return JsonResponse({"denied":'Failed request', "message" : 'You are not authorized!'})


# ===================================================


def new_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)

        if form.is_valid():
            form.instance.owner = request.user
            form.save()
        messages.success(request, "Folder created", fail_silently=True)
        return HttpResponseRedirect(reverse('vault:index'))

# ===================================================


def edit_folder(request, id):
    """from async request GET method returns name of folder if present
        PUT request, gets body content of input field and assigns to the model
        DELETE request deletes the db entry"""

    # on fetch get request to get the pre filled field checks if folder exists and if request.user is owner
    # protection for html hacking
    try:
        folder = Folder.objects.get(id=id)
    except:
        return JsonResponse({"denied": "request denied", "message":"Folder does not exist"})

    if folder.owner != request.user:
        return JsonResponse({"denied":"request denied", "message":"You are not the owner!"})

    if request.method == "PUT":
        new_name = json.loads(request.body)
        folder.name = new_name
        folder.save()

        return JsonResponse({"success":"successful request", "message":"Folder edited"})



    elif request.method == "DELETE":
        folder.delete()
        return JsonResponse({"success":"successful request", "message":"folder deleted"})

    # else : GET send name and color as json
    return JsonResponse({"success": "successful request", "name": folder.name, "id": folder.id})


