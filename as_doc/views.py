#   login handler 
from django.contrib.auth import authenticate, login, logout
#---------------------------------
#       view output
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
#--------------------------------------------------------
#      views constraint
from django.contrib.auth.decorators import login_required
#--------------------------------------------------------
#       Exceptions
from django.db import IntegrityError
#-------------------------------
#       User Model
from django.contrib.auth import get_user_model
User = get_user_model()
#------------------------------
# Appointment Model
from reception.models import Appointment
#-------------------------------
#      Utility Functions
from projectH import utils
#--------------------------------

def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(user_id=request.user.user_id)
        doctor_appointments = user.assigned_patients.all().exclude(status='D')
        # print(user.firstname,user.lastname)
        # active appointment will show first
        # doctor_appointments.sort(key=lambda x: x.status, reverse=True)
        doctor_appointments = sorted(doctor_appointments, key=lambda x: x.date,reverse=True)
        return render(request,"as_doc/appointment.html",
        {
            "doctor":user,
            "appointments":doctor_appointments,
            "current_year":utils.get_year(),
        })
    else:
        return HttpResponseRedirect(reverse("as_doc:login"))

def as_doclogin(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('as_doc:index'))
        else:
            return render(
                request,
                "as_doc/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "as_doc/login.html")

def as_doclogout(request):
    logout(request)
    return HttpResponseRedirect(reverse("as_doc:index"))

def as_docregister(request):
    if request.method == "POST":
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        email = request.POST["email"]
        contact = request.POST["primarycontact"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        alternate_contact = request.POST["alternatecontact"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        address=""

        # Ensure password matches confirmation
        if not utils.validate_password(password,confirmation):
            return render(
                request, "as_doc/register.html", {"message": "Passwords must match."}
            )
                # generate user id
        id_list=[]
        while(True):
            user_id =utils.uid_gen()
            id_list = User.objects.filter(user_id=user_id)
            # if user id is unique then take it
            # otherwise generate user id again
            if(len(id_list)==0):
                break
        # Attempt to create new user, if user already exists ,raises integrity error
        try:
            # print(f"{name}\n {email}\n {contact}\n {alternate_contact}\n {password} and {confirmation}\n {dob}\n {gender}")
            user = User.objects.create_as_doc(
                firstname=firstname,
                lastname= lastname, 
                email=email,
                password=password,          
                primary_contact=contact,
                user_id=user_id,
                alternate_contact=alternate_contact,
                gender = gender,
                dob=dob,
                address=address,
                )
            user.save()
        except IntegrityError:
            return render(
                request,
                "as_doc/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("as_doc:index"))
    else:
        return render(request, "as_doc/register.html")

@login_required(login_url="login")
def status(request):
    user = User.objects.get(user_id=request.user.user_id)
    if request.method=='GET':
        return render(request,
        "as_doc/status.html",{
            "doctor":user,

        })
    elif request.method=='POST':
        status = request.POST["status"]

        user.status = status
        user.save()
        
        return HttpResponseRedirect(reverse("as_doc:index"))

@login_required(login_url="login")
def edit_appointment(request,id):
    appointment = Appointment.objects.get(appointment_id=id)
    if request.method=="GET":
        return render(request,
        "as_doc/edit-appointment.html",{
            "appointment":appointment,
            "date":utils.date_to_string(appointment.date),
			"time":utils.time_to_str(appointment.time) +" "+ appointment.am_pm,
        })
    elif request.method == "POST":
        status = request.POST["status"]
        message =request.POST["message"]

        appointment.status = status
        appointment.message = message
        appointment.save()
        return HttpResponseRedirect(reverse("as_doc:index"))


@login_required(login_url="login")
def archive(request):
    user = User.objects.get(user_id=request.user.user_id)
    doctor_archive_appointments = user.assigned_patients.filter(status='D')
    return render(request,
    "as_doc/archive-appointment.html",{
            "doctor":user,
            "appointments":doctor_archive_appointments,
            "current_year":utils.get_year(),
    })

def edit_archive_appointment(request,id):
    appointment = Appointment.objects.get(appointment_id=id)
    if request.method == "GET":
        return render(request,
        "as_doc/edit-archive-appointment.html",{
            "appointment":appointment,
            "date":utils.date_to_string(appointment.date),
			"time":utils.time_to_str(appointment.time) +" "+ appointment.am_pm,
        })
    elif request.method == "POST":
        status = request.POST["status"]
        message =request.POST["message"]

        appointment.status = status
        appointment.message = message
        appointment.save()
        return HttpResponseRedirect(reverse("as_doc:archive"))