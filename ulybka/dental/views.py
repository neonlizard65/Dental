from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
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
    
def login_page(request):
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
            for field in form:
                if field.errors:
                    print("Field Error:", field.name,  field.errors)
            return render(request, "register.html", {"form": form})     
    elif request.method == 'GET':
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


@login_required(login_url='/login')
def cabinet(request):
    pass
