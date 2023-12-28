from django.urls import path
from . import views

app_name = 'patient'
urlpatterns=[
    path("",views.index,name="index"),
    path("plogin/",views.patient_login,name="plogin"),
    path("plogout/",views.patient_logout,name="plogout"),
    path("pregister/",views.patient_register,name="pregister"),
    path("forgot-password/",views.forgot_pswd,name="forgotpswd"),
    path("<str:userid>/diseases",views.associateOfDiseases,name="associateOfDiseases"),
]