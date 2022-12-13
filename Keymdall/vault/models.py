from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

from dashboard.models import User
from .encrypt_util import encrypt, decrypt




class Login(models.Model):
    """ Login model only required field is title, field encryption is managed in backend"""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=80)
    username = models.CharField(max_length=80, null=True, blank=True)
    password = models.CharField(max_length=80, null=True, blank=True)
    note = models.TextField(max_length=500, null=True, blank=True)
    folder = models.ForeignKey("Folder", on_delete=models.SET_NULL, null=True, blank=True, related_name="folder")
    protected = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="entries")
    uri = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.title

    @property
    def passw_history(self):
        return History.objects.filter(login=self)

    @property
    def folderColor(self):
        return self.folder.color


class History(models.Model):
    """ Stores former Login password fields when updated by user """
    id = models.BigAutoField(primary_key=True)
    old_passw = models.CharField(max_length=80)
    login = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="previous_password")


    def __str__(self):
        return self.old_passw

# fixed set of colors accents for Folders
COLOR_CHOICES = (
    ('teal','TEAL'),
    ('green','GREEN'),
    ('emerald','EMERALD'),
    ('blue', 'BLUE'),
    ('cyan', 'CYAN'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('violet','VIOLET'),
    ('pink','PINK'),
    ('yellow','YELLOW'),
)

class Folder(models.Model):
    """ Folder to organize Logins/Items, default color is cyan, user has 10 color choices"""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    color = models.CharField(max_length=8,choices=COLOR_CHOICES, default='cyan')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="folders")

    def __str__(self):
        return self.name
