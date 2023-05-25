from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name=""),
    path("about", views.about),
    path("doctors", views.doctors),
    path("contacts", views.contacts),
    path("law", views.law),
    path("requisites", views.requisites),
    path("register", views.register_page),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("cabinet", views.cabinet, name="cabinet"),
    path("zapis", views.zapis, name='zapis'),
    path("get/schedule", views.get_schedule),
    path("post/visit", views.post_visit)
] 
