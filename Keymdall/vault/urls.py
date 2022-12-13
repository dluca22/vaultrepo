from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
    path("", views.index, name="index"),
    path("add_new", views.add_new, name="add_new"),
    path("password/<int:id>", views.get_password, name="password"),
    path("login/<int:id>", views.login_content, name="login_content"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("new_folder", views.new_folder, name="new_folder"),
    path("edit_folder/<int:id>", views.edit_folder, name="edit_folder"),
    path('generate_password/<int:size>', views.generate_password, name="generator"),

]