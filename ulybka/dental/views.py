from django.shortcuts import render
from .models import Doctor
from .forms import RegisterForm, LoginForm


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def doctors(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, "doctors.html", context = context)

def law(request):
    return render(request, "law.html")

def contacts(request):
    return render(request, "contacts.html")

def requisites(request):
    return render(request, "requisites.html")
    
def login(request):
    form = LoginForm()
    return render(request, "login.html", {"form": form})

def register(request):
    form = RegisterForm()
    return render(request, "register.html", {"form": form})

