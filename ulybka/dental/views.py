import datetime
from tracemalloc import start
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Doctor, Patient, Schedule, Visit
from .forms import RegisterForm, LoginForm, EditUserForm


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
        form = RegisterForm(request.POST, request.FILES)
        form.photo = request.FILES['photo']
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
def cabinet(request: HttpRequest):
    user_data = Patient.objects.get(id = request.user.id)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance = request.user)
        
        if form.is_valid():
            messages.success(request, 'Учётная запись обновлена')
            user = form.save()
            
            return render(request, "cabinet.html", context = {'form': form, 'data': user_data})
        else:
            print("hello")
            return render(request, "cabinet.html", context = {'form': form, 'data': user_data})
    else: 
        form = EditUserForm(instance = request.user)
        print(user_data)
        return render(request, "cabinet.html", context = {'form': form, 'data': user_data})

def logout_page(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/login')
def zapis(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'zapis.html', context = context)

def get_schedule(request: HttpRequest):
    if request.GET.get('doctor'):
        doctor = request.GET.get('doctor')
        doctor_obj = Doctor.objects.filter(id = doctor).first()
        schedule = doctor_obj.times.all()
        visits = Visit.objects.filter(doctor = doctor)
        
        
        for visit in visits:
            if visit.datetime.date() >= datetime.date.today():
                for time in schedule:
                    time:Schedule
                    if visit.datetime.time().hour == int(time.start_time.split(':')[0]) and visit.datetime.time().minute == int(time.start_time.split(':')[1]):
                        day_of_week_n = visit.datetime.weekday()
                        day_of_week: str
                        if day_of_week_n == 0:
                            day_of_week = 'Понедельник'
                        elif day_of_week_n == 1:
                            day_of_week = 'Вторник'
                        elif day_of_week_n == 2:
                            day_of_week = 'Среда' 
                        elif day_of_week_n == 3:
                            day_of_week = 'Четверг'
                        elif day_of_week_n == 4:
                            day_of_week = 'Пятница'
                        elif day_of_week_n == 5:
                            day_of_week = 'Суббота'
                        elif day_of_week_n == 6:
                            day_of_week = 'Восресенье'
                        schedule = schedule.exclude(day_of_week = day_of_week, start_time = time.start_time)
        
        print(schedule)
        
        schedule_values = list(schedule.values('id', 'day_of_week', 'start_time', 'end_time'))
        
        schedule_data = {"schedule" : schedule_values}
        return JsonResponse(schedule_data)
    else:
        return JsonResponse({"schedule": []})
    
def post_visit(request: HttpRequest):
    if request.method == 'POST':
        scheduleid = request.POST['time']
        doctorid = request.POST['doctor']
                
        schedule:Schedule = Schedule.objects.filter(id = scheduleid).first()
        
        temp_date = datetime.datetime.today()
        end_date = datetime.datetime.today().__add__(datetime.timedelta(7))
        
        while(temp_date < end_date):
            
            day_of_week_n = temp_date.weekday()
            day_of_week: str
            if day_of_week_n == 0:
                day_of_week = 'Понедельник'
            elif day_of_week_n == 1:
                day_of_week = 'Вторник'
            elif day_of_week_n == 2:
                day_of_week = 'Среда' 
            elif day_of_week_n == 3:
                day_of_week = 'Четверг'
            elif day_of_week_n == 4:
                day_of_week = 'Пятница'
            elif day_of_week_n == 5:
                day_of_week = 'Суббота'
            elif day_of_week_n == 6:
                day_of_week = 'Восресенье'
                
            if schedule.day_of_week == day_of_week:
                hours = int(schedule.start_time.split(':')[0])
                minutes = int(schedule.start_time.split(':')[1])
                print(hours, minutes)
                temp_date = temp_date.replace(hour = hours, minute = minutes, second=0)
                visit = Visit.objects.create(doctor = Doctor.objects.get(id = doctorid), patient = Patient.objects.get(id = request.user.id), datetime = temp_date)
                break
            else:
                temp_date = temp_date.__add__(datetime.timedelta(1))
            
            
        return render(request, "success.html")