from typing import Any, Optional
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.db.models.query import QuerySet
from django.db.models import Case, When, Value
from django.contrib.auth.models import AbstractUser
from django.http.request import HttpRequest
from .models import Visit, Doctor, Patient, Schedule, Specialty, ToothCard
class SpecialityListFilter(SimpleListFilter):
    
    title = "Специальности"
    
    parameter_name = "Специальность"
    
    def lookups(self, request, model_admin):
        return (
            (1, 'Имплантолог'),
            (2, 'Стоматолог-хирург'),
            (3, 'Ортодонт')
        )
        
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        
        if self.value() == '1':
            return queryset.filter(speciality = 1)
        elif self.value() == '2':
            return queryset.filter(speciality = 2)
        elif self.value() == '3':
            return queryset.filter(speciality = 3)    
        
        

class DoctorAdmin(UserAdmin):
    list_display = ('last_name', 'first_name', 'patronym', 'speciality',)

    fieldsets = (
        (None, {
            "fields": (
                'last_name', 'first_name', 'patronym', 'speciality', 'times', 'email', 'password', 'dob', 'photo', 'is_staff', 'is_active'
            ),
        }),
    )
    
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
    

class PatientAdmin(UserAdmin):
    list_display = ('__str__',)
    
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
    
    ordering = ('last_name', 'first_name', 'patronym', 'phone', 'email', 'password', 'dob', 'is_staff', 'is_active')

admin.site.register(Visit)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Schedule)
admin.site.register(Specialty)
admin.site.register(ToothCard)
