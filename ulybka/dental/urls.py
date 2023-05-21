from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("about", views.about),
    path("doctors", views.doctors),
    path("contacts", views.contacts),
    path("law", views.law),
    path("requisites", views.requisites),
    path("register", views.register),
    path("login", views.login),
] 
