from django.urls import path
from . import views

app_name = 'reception'
urlpatterns=[

    path("",views.index,name='index'),
    path("login/",views.reception_login,name="login"),
    path("logout/",views.reception_logout,name="logout"),
#   doctors
    path("doctors/",views.show_doctors,name="show_doctors"),
    path("add-doctor/",views.add_doctor,name="add_doctor"),
    path("<str:id>/edit-doctor/",views.edit_doctor,name="edit_doctor"),
    path("<str:id>/delete-doctor/",views.delete_doctor,name="delete_doctor"),
    path("<str:id>/update-doctor-password/",views.update_doctor_password,name="update_doctor_password"),
#   patients
    path("patients/",views.show_patients,name="show_patients"),
    path("add-patient/",views.add_patient,name="add_patient"),
    path("<str:id>/edit-patient/",views.edit_patient,name="edit_patient"),
    path("<str:id>/delete-patient/",views.delete_patient,name="delete_patient"),
    path("<str:id>/update-patient-password/",views.update_patient_password,name="update_patient_password"),

    # appointments
    path("appointments/",views.show_appointments,name="show_appointments"),
    path("add-appointment/",views.add_appointment,name="add_appointment"),
    path("<str:appointment_id>/edit-appointment/",views.edit_appointment,name="edit_appointment"),
    path("<str:appointment_id>/delete-appointment/",views.delete_appointment,name="delete_appointment"),

    # archives
    path("archive-appointment/",views.show_archive_appointments,name="show_archive_appointments"),
    path("<str:appointment_id>/archive_appointment/",views.archive_appointment,name="archive_appointment"),
    path("<str:appointment_id>/unarchive_appointment/",views.unarchive_appointment,name="unarchive_appointment"),
    path("<str:appointment_id>/edit_unarchive_appointment/",views.edit_archive_appointment,name="edit_archive_appointment"),


    # Doctor Schedule
    path("schedules/",views.show_doctor_schedules,name="show_doctor_schedules"),
    path("add-schedule/",views.add_doctor_schedule,name="add_doctor_schedule"),
    path("<int:id>/edit-schedule/",views.edit_doctor_schedule,name="edit_doctor_schedule"),
    path("<int:id>/delete-schedule/",views.delete_doctor_schedule,name="delete_doctor_schedule"),


    
]