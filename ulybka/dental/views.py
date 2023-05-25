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

#Здесь код для отображения данных на страницах html

#Главная
def index(request):
    return render(request, "index.html")

#О клинике
def about(request):
    return render(request, "about.html")

#Врачи
def doctors(request):
    doctors = Doctor.objects.all() #Берем данные из БД
    context = {'doctors': doctors} #Создаем контекст
    return render(request, "doctors.html", context = context) #Передаем контекст html странице
 
#Правовая информация
def law(request):
    return render(request, "law.html")

#Контакты
def contacts(request):
    return render(request, "contacts.html")

#Реквизиты
def requisites(request):
    return render(request, "requisites.html")
    

#Авторизация
def login_page(request: HttpRequest):
    #Если отправлен POST запрос, т.е. нажата кнопка войти
    if request.method == 'POST':
        form = LoginForm(data = request.POST) #Обрабатываем и записываем форму в переменную
        
        #Если форма корректно заполнена
        if form.is_valid():
            user = form.get_user() #Получаем пользователя
            #Если пользователь существует и не заблокирован системой
            if user is not None and user.is_active:
                login(request, user) #Авторизация
                return redirect('cabinet') #Переход на страницу личного кабинета
            else:
                messages.error(request, "Неверно указана почта или пароль") #Передаем в html сообщение об ошибке
        else:
            messages.error(request, "Неверно указана почта или пароль")
         
            
    else:
        form = LoginForm() #Если GET запрос, выводим страницу по умолчанию
        
    return render(request, "login.html", {"form": form})

#Регистрация
def register_page(request: HttpRequest):
    #Если отправлена форма
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES) #Получаем данные и файлы
        #Если форма корректно заполнена
        if form.is_valid():
            patient = form.save() #Записываем пациента в БД
            messages.success(request, "Успешная регистрация") #Сообщение
            login(request, patient) #Авторизация
            return redirect('') #На главную
        else:
            return render(request, "register.html", {"form": form}) #Обновление страницы со списком ошибок, если не пройдена валидация формы
    #Если GET запрос     
    elif request.method == 'GET':
        form = RegisterForm() #Выводим незаполненную форму
        return render(request, "register.html", {"form": form})


#Личный кабинет (нужно быть авторизованным, иначе редирект на login)
@login_required(login_url='/login')
def cabinet(request: HttpRequest):
    user_data = Patient.objects.get(id = request.user.id) #Получаем данные пациента по id
    #Если нажали на обновить данные
    if request.method == "POST":
        form = EditUserForm(request.POST, instance = request.user) #Считываение формы
        
        #Проверка на валидность
        if form.is_valid():
            messages.success(request, 'Учётная запись обновлена')
            user = form.save() #Сохранение изменений
            
            return render(request, "cabinet.html", context = {'form': form, 'data': user_data})
        else:
            return render(request, "cabinet.html", context = {'form': form, 'data': user_data})
    else: 
        #get
        form = EditUserForm(instance = request.user)
        return render(request, "cabinet.html", context = {'form': form, 'data': user_data})

#Выход из учетной записи
def logout_page(request):
    logout(request)
    return redirect("/")

#Запись на прием
@login_required(login_url='/login')
def zapis(request):
    doctors = Doctor.objects.all() #Получаем и выводим список врачей. Расписание сделано в отдельном js файле
    context = {'doctors': doctors}
    return render(request, 'zapis.html', context = context)

#Метод API для получения расписания конкретного врача. Его использует js
def get_schedule(request: HttpRequest):
    #127.0.0.1:8000/get/schedule?doctor=3
    #Если передан параметр Get запроса "doctor"
    if request.GET.get('doctor'):
        doctor = request.GET.get('doctor') #Получаем id, которое передано в get запросе
        doctor_obj = Doctor.objects.filter(id = doctor).first() #Получаем объект врача
        schedule = doctor_obj.times.all() #Получаем расписание врача
        visits = Visit.objects.filter(doctor = doctor) #Получаем приемы
        
        #Проверяем все приемы, чтобы проверить свободные времена для приема
        for visit in visits:
            if visit.datetime.date() >= datetime.date.today(): #Будем проверять только будущие приемы
                #Проверяем все времена, в которые принимает врач
                for time in schedule:
                    time:Schedule
                    #Если время и день совпадают с временем приема, то исключаем его из расписания
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
        
        schedule_values = list(schedule.values('id', 'day_of_week', 'start_time', 'end_time'))
        
        schedule_data = {"schedule" : schedule_values}
        return JsonResponse(schedule_data) #Вывод расписания в JSON
    else:
        return JsonResponse({"schedule": []}) #Вывод пустого расписания в JSON
    
#Запись на прием. Заполняем все поля модели Visit (Врач, Пациент, Время и дата приема)
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