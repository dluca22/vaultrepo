from django.contrib import admin

# Register your models here.
from .models import Login, Folder, History

admin.site.register(Login)
admin.site.register(Folder)
admin.site.register(History)