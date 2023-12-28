from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()


DAYS_CHOICES = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)
APPOINTMENT_CHOICES = (
    ('A', 'Active'),
    ('C', 'Confirmed'),
    ('D', 'Done'),
)

class DaysOfTheWeek(models.Model):
    available_days = models.CharField(max_length=9,choices=DAYS_CHOICES,null=True)

    def __str__(self):
        return f"{self.available_days}"

# Doctors schedule 
class Schedule(models.Model):
    doctor= models.ForeignKey(User,on_delete=models.CASCADE,related_name='schedules',null=True)
    working_days = models.ManyToManyField(DaysOfTheWeek)
    available_time_from = models.TimeField(auto_now=False,auto_now_add=False,null=True)
    from_am_pm = models.CharField(max_length=2,null=True)
    available_time_to = models.TimeField(auto_now=False,auto_now_add=False,null=True)
    to_am_pm = models.CharField(max_length=2,null=True)
    message = models.TextField(max_length=1000,null=True)
    #  taking 'schedule status' from the assigned doctor(users) status

    def __str__(self):
        return f"{self.doctor.firstname} {self.doctor.lastname} -> {self.working_days.filter()}\n"

# Patient Appointments
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=4,null=True)
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='appointments')
    # take patient age from patient_name(user)
    
    doctor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_patients')
    date = models.DateField(auto_now=False,auto_now_add=False,null=True)
    time = models.TimeField(auto_now=False,auto_now_add=False,null=True)
    am_pm = models.CharField(max_length=2,null=True)
    message = models.TextField(max_length=1000,null=True)
    # status = models.BooleanField(default=False)
    status = models.CharField(max_length=1,choices=APPOINTMENT_CHOICES,null=True,blank=True)

    def __str__(self):
        return f"ID : {self.appointment_id} {self.patient.firstname} {self.patient.lastname} -> {self.doctor.firstname} {self.doctor.lastname}"
