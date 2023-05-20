from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

days_of_week = ((0, "Понедельник"), (1, "Вторник"), (2, "Среда"), (3, "Четверг"), (4, "Пятница"), (5, "Суббота"), (6, "Воскресенье"))

class Specialty(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    about = models.CharField(max_length=150, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"
        
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
class CommonUser(AbstractUser):
    patronym = models.CharField(max_length=30, verbose_name="Отчество", null=True)
    dob = models.DateField(verbose_name="Дата рождения", null=True)
    photo = models.ImageField(verbose_name="Фотография", null=True)
    
class Schedule(models.Model):
    day_of_week =  models.CharField(choices=days_of_week, verbose_name="День недели:")
    start_time = models.CharField(max_length=5, verbose_name="Начало приема: ")
    end_time = models.CharField(max_length=5, verbose_name="Конец приема: ")
    
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"
        
    def __repr__(self) -> str:
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"
    
    def __str__(self) -> str:
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"
    
    
class Doctor(CommonUser):
    speciality = models.ForeignKey(Specialty, verbose_name="Специальность", on_delete=models.CASCADE)
    times = models.ManyToManyField(Schedule, verbose_name="Расписание")
    
    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __repr__(self) -> str:
        return f"Врач - {self.user.last_name} {self.user.first_name} {self.patronym}"
    
    def __str__(self) -> str:
        return f"Врач - {self.last_name} {self.first_name} {self.patronym}"

class Patient(CommonUser):
    phone = PhoneNumberField(verbose_name = "Номер телефона", unique=True)
    
    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __repr__(self) -> str:
        return f"Пациент - {self.last_name} {self.first_name} {self.patronym}"
    
    def __str__(self) -> str:
        return f"Пациент - {self.last_name} {self.first_name} {self.patronym}"

class Visit(models.Model):
    doctor = models.ForeignKey(Doctor, verbose_name="Врач", on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE)
    datetime = models.DateTimeField(verbose_name="Время приема")
   
    class Meta:
        verbose_name = "Прием"
        verbose_name_plural = "Приемы"

    def __repr__(self) -> str:
        return f"({self.datetime}) {self.patient.last_name} - {self.doctor.last_name}"
    
    def __str__(self) -> str:
        return f"({self.datetime}) {self.patient.last_name} - {self.doctor.last_name}"

class ToothCard(models.Model):
    patient = patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE)
    datetime = models.DateTimeField(verbose_name="Время приема")
    diagnosis = models.CharField(max_length=50, verbose_name="Диагноз")
    healing = models.CharField(max_length=150, verbose_name="Лечение")

    class Meta:
        verbose_name = "Зубная карта пациента"
        verbose_name_plural = "Зубная карта пациента"
        
    def __repr__(self) -> str:
        return f"({self.datetime}) {self.diagnosis} - {self.healing}"
    
    def __str__(self) -> str:
        return f"({self.datetime}) {self.diagnosis} - {self.healing}"
    