from typing import Any, Optional
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.db.models.query import QuerySet
from django.db.models import Case, When, Value
from django.contrib.auth.models import AbstractUser
from django.http.request import HttpRequest
from .models import Visit, Doctor, Patient, Schedule, Specialty, ToothCard

#Класс для фильтра врачей по специальности
class SpecialityListFilter(SimpleListFilter):
    
    title = "Специальности"
    
    parameter_name = "Специальность"
    
    def lookups(self, request, model_admin):
        return (
            (1, 'Имплантолог'),
            (2, 'Стоматолог-хирург'),
            (3, 'Ортодонт'),
            (4, 'Эндодонтист')
        )
        
    #Логика отбора по каждой специальности
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        
        if self.value() == '1':
            return queryset.filter(speciality = 1)
        elif self.value() == '2':
            return queryset.filter(speciality = 2)
        elif self.value() == '3':
            return queryset.filter(speciality = 3)    
        elif self.value() == '4':
            return queryset.filter(speciality = 4)   
        
        
#Класс для кастомной админ панели врача
class DoctorAdmin(UserAdmin):
    #Какие поля показываются в форме списка
    list_display = ('last_name', 'first_name', 'patronym', 'speciality',)

    #Какие поля показываются на форме элемента
    fieldsets = (
        (None, {
            "fields": (
                'last_name', 'first_name', 'patronym', 'speciality', 'times', 'email', 'password', 'dob', 'photo', 'is_staff', 'is_active'
            ),
        }),
    )
    
    #Какие поля показываются на форме создания нового элемента
    add_fieldsets = (
        (None, {
            "fields": (
                'last_name', 'first_name', 'patronym', 'speciality', 'times', 'email', 'password1', 'password2', 'dob', 'photo', 'is_staff', 'is_active'
            ),
        }),
    )
    
    search_fields = ['last_name'] #Поиск по фамилии
    
    list_filter = [SpecialityListFilter] #Фильтр по специальности
    
    ordering = ['date_joined'] #Порядок вывода врачей
    

#Класс для кастомной админ-панели пациента
class PatientAdmin(UserAdmin):
    list_display = ('__str__',) #Выводит их в формате, который задан функцией __str__у класса Patient
    
    fieldsets = (
        (None, {
            "fields": (
                'last_name', 'first_name', 'patronym', 'phone', 'email', 'password', 'dob', 'photo', 'is_staff', 'is_active'
            ),
        }),
    )
    
    add_fieldsets = (
        (None, {
            "fields": (
                'last_name', 'first_name', 'patronym', 'phone', 'email', 'password', 'dob', 'photo', 'is_staff', 'is_active'
            ),
        }),
    )
    
    #Порядок, по которому сортируются пациенты
    ordering = ('last_name', 'first_name', 'patronym', 'phone', 'email', 'password', 'dob', 'is_staff', 'is_active')

#Добавляем все модели на админ панель
admin.site.register(Visit)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Schedule)
admin.site.register(Specialty)
admin.site.register(ToothCard)
