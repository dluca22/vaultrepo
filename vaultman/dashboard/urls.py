from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login", views.login_form, name="login"),
    path("register", views.register_form, name="register"),
    path("logout", views.logout_user, name="logout"),
    path("edit_pin", views.edit_pin, name="edit_pin"),
    path("set_pin", views.set_pin, name="set_pin"),
    path("change_masterpassword", views.change_masterpassword, name="change_masterpassword"),
    path("change_email", views.change_email, name="change_email"),
    path("delete_account", views.delete_account, name="delete_account"),


]