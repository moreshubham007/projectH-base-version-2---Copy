from django.urls import path
from . import views

app_name = 'as_doc'
urlpatterns=[
    path("",views.index,name="index"),
    path("login/",views.as_doclogin,name="login"),
    path("register/",views.as_docregister,name="register"),
    path("logout/",views.as_doclogout,name="logout"),
    path("status/",views.status,name="status"),
    path("<str:id>/edit_appointment",views.edit_appointment,name="edit_appointment"),
    path("archive/",views.archive,name="archive"),
    path("<str:id>/edit_archive_appointment",views.edit_archive_appointment,name="edit_archive_appointment"),
]