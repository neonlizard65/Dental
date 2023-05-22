from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("about", views.about),
    path("doctors", views.doctors),
    path("contacts", views.contacts),
    path("law", views.law),
    path("requisites", views.requisites),
    path("register", views.register_page),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("cabinet", views.cabinet, name="cabinet")
] 
