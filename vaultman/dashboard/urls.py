from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("edit/<str:field>", views.edit, name="edit"),
    path("login", views.login_form, name="login"),
    path("register", views.register_form, name="register"),
    path("logout", views.logout_user, name="logout"),


]