from django.db import models

# from colorfield.fields import ColorField




class Login(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=False, null=False)
    username = models.CharField(max_length=80, null=True, blank=True)
    password = models.CharField(max_length=80, null=True, blank=True)
    note = models.TextField(max_length=500, null=True, blank=True)
    folder = models.ForeignKey("Folder", on_delete=models.SET_NULL, null=True, blank=True, related_name="folder") #LATER change name
    protected = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="entries")
    uri = models.CharField(max_length=100, null=True, blank=True)
