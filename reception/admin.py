from django.contrib import admin
from .models import Schedule,DaysOfTheWeek,Appointment
# Register your models here.
admin.site.register(Schedule)
admin.site.register(DaysOfTheWeek)
admin.site.register(Appointment)