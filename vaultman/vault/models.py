from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

from dashboard.models import User




class Login(models.Model):
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
    def has_history(self):
        return History.objects.filter(login=self)

    @property
    def folderColor(self):
        return self.folder.color



class History(models.Model):
    id = models.BigAutoField(primary_key=True)
    old_passw = models.CharField(max_length=80)
    login = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="previous_password")


    def __str__(self):
        return self.old_passw


COLOR_CHOICES = (
    ('teal','TEAL'),
    ('green','GREEN'),
    ('emerald','EMERALD'),
    ('blue', 'BLUE'),
    ('cyan', 'CYAN'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
    ('violet','VIOLET'),
    ('pink','PINK'),
    ('yellow','YELLOW'),
)

class Folder(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    color = models.CharField(max_length=8,choices=COLOR_CHOICES, default='cyan')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="folders")

    def __str__(self):
        return self.name
