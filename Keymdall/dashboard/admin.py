from django.contrib import admin

# Register your models here.

from vault.models import Login, Folder, History
from dashboard.models import User

admin.site.register(Login)
admin.site.register(Folder)
admin.site.register(User)
admin.site.register(History)