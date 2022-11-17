from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
    path("", views.index, name="index"),
    path("add_new", views.add_new, name="add_new"),
    path("password", views.get_password, name="password"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("delete/<int:id>", views.delete, name="delete"),

]