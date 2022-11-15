from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator




class User(AbstractUser):
    username = models.CharField(max_length=80, null=False, blank=False)
    email = models.EmailField( unique=True)
    pin = models.PositiveIntegerField(validators=[MaxValueValidator(9999)], null=True, blank=True)

    USERNAME_FIELD: "email"

    def __str__(self):
        return self.username