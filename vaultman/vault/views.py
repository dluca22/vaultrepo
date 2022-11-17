from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib import messages
import json

from .models import Login, History ,Folder
from .forms import LoginForm, FolderForm


# Create your views here.

@login_required(login_url=reverse_lazy('dashboard:login'), redirect_field_name=None)
def index(request):

    login_form = LoginForm()
    logins = Login.objects.filter(owner=request.user)
    context = {'logins':logins, 'form':login_form}
    return render(request, 'vault/index.html', context=context)

def add_new(request):
    """add <str:type> per aggiungere sia login che note"""
    if request.method == "POST":
        return
    else:
        HttpResponseRedirect(reverse('vault:index'))


def get_password(request):
    """ fare controllo se il login è protected presentare richiesta pin"""
    pass


def edit(request, id):
    """edita il field """
    # MAYBE convertire id a hex ??
    pass


def delete(request,id):
    """cancella l'elemento """
    # MAYBE convertire id a hex ??
    pass