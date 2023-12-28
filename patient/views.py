#   login handler 
from django.contrib.auth import authenticate, login, logout
#---------------------------------
#       view output
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
#------------------------------
#       Exceptions
from django.db import IntegrityError
#-------------------------------
#       User Model
from django.contrib.auth import get_user_model
User = get_user_model()
#------------------------------
#      Utility Functions
from projectH import utils
#--------------------------------

def index(request):
    if request.user.is_authenticated:
        return render(request,"patient/customer-dashboard.html")
    else:
        return HttpResponseRedirect(reverse("patient:plogin"))

def patient_login(request):
    # already signed-in user cannot go to login page
    if request.user.is_authenticated:
        return render(request,"patient/customer-dashboard.html")

    elif request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        # print(user)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('patient:index'))
        else:
            return render(
                request,
                "patient/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "patient/login.html")


def patient_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("patient:index"))

def patient_register(request): 
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
        address=request.POST["address"]
        # new patient type by default
        patient_type = 'N'
        # Ensure password matches confirmation
        if not utils.validate_password(password,confirmation):
            return render(
                request, "patient/register.html", {"message": "Passwords must match."}
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
            print(f"{user_id}\n {firstname}\n {lastname}\n {email}\n {contact}\n {alternate_contact}\n {password} and {confirmation}\n {dob}\n {gender}")
            user = User.objects.create_user(
                firstname=firstname,
                lastname= lastname, 
                email=email,
                password=password,    
                user_id=user_id,      
                primary_contact=contact,
                alternate_contact=alternate_contact,
                gender = gender,
                dob=dob,
                address=address,
                )
            user.patient_type=patient_type
            user.save()
        except IntegrityError:
            return render(
                request,
                "patient/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("patient:index"))
    else:
        return render(request, "patient/register.html")

def forgot_pswd(request):
    return render(
        request,
        "patient/forgot-password.html"
    )

def associateOfDiseases(request,userid):
    user_diseases = User.objects.get(user_id=userid)
    print(user_diseases)
    return render(request,
    "patient/associate-diseases.html")