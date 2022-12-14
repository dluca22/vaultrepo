from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

from vault.encrypt_util import decrypt



class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=80, null=False, blank=False, unique=True)
    pin = models.CharField(max_length=6, validators=[MinLengthValidator(4)], null=True, blank=True)
    # TODO IMPORTANT change to CharFiled to enable hashing and add validators in the input field

    USERNAME_FIELD: 'username'

    def __str__(self):
        return self.username

    @property
    def num_logins(self):
        return self.entries.all().count()

    @property
    def num_folders(self):
        return self.folders.all().count()

    @property
    def get_pin(self):
        return decrypt(self.pin)
