from django.contrib import admin
from .models import Visit, Doctor, Patient, Schedule, Specialty, ToothCard

admin.site.register(Visit)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Schedule)
admin.site.register(Specialty)
admin.site.register(ToothCard)
