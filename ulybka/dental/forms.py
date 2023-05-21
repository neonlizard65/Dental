from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Patient


class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = Patient
        fields = ("last_name", "first_name", "patronym", "dob", "email", 'photo', "password1", "password2")