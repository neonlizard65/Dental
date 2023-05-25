from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import Patient
from phonenumber_field.formfields import PhoneNumberField
from django.utils.safestring import mark_safe


class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = Patient
        fields = ("last_name", "first_name", "patronym", "dob", "email", "phone", 'photo', "password1", "password2")
        
class EditUserForm(UserChangeForm):
    password = None
    class Meta:
        model = Patient
        fields = ("last_name", "first_name", "patronym", "dob", "email")
        