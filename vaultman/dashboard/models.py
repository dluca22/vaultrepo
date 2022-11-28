from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator





class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=80, null=False, blank=False, unique=True)
    pin = models.CharField(max_length=6, validators=[MinLengthValidator(4)], null=True, blank=True)
    # TODO IMPORTANT change to CharFiled to enable hashing and add validators in the input field

    USERNAME_FIELD: 'email'

    def __str__(self):
        return self.username

