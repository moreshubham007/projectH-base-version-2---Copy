from django.urls import path
from . import views

app_name = 'admin_doc'
urlpatterns=[
    path("",views.index,name="index"),
    path("login/",views.admin_doc_login,name="login"),
    path("logout/",views.admin_doc_logout,name="logout"),
    path("register/",views.admin_doc_register,name="register"),
]