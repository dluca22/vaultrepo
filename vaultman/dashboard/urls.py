from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("edit/<str:field>", views.edit, name="edit"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path('', include("vault.urls", namespace='vault')),


]