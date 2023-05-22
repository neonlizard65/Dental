from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
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
    
def login_page(request: HttpRequest):
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_active:
                login(request, user)
                return redirect('cabinet')
            else:
                messages.error(request, "Неверно указана почта или пароль")
        else:
            messages.error(request, "Неверно указана почта или пароль")
         
            
    else:
        form = LoginForm()
        
    return render(request, "login.html", {"form": form})


def register_page(request: HttpRequest):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, "Успешная регистрация")
            login(request, patient)
            return redirect('')
        else:
            return render(request, "register.html", {"form": form})     
    elif request.method == 'GET':
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


@login_required(login_url='/login')
def cabinet(request):
    return render(request, "cabinet.html")

def logout_page(request):
    logout(request)
    return redirect("/")