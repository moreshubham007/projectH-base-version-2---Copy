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
        return render(request,"admin_doc/index.html")
    else:
        return HttpResponseRedirect(reverse("admin_doc:login"))

def admin_doc_login(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('admin_doc:index'))
        else:
            return render(
                request,
                "as_doc/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "admin_doc/login.html")

def admin_doc_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("admin_doc:index"))

def admin_doc_register(request):
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


        # generate user id
        id_list=[]
        while(True):
            user_id =utils.uid_gen()
            id_list = User.objects.filter(user_id=user_id)
            # if user id is unique then take it
            # otherwise generate user id again
            if(len(id_list)==0):
                break
        
        # Ensure password matches confirmation
        if not utils.validate_password(password,confirmation):
            return render(
                request, "admin_doc/register.html", {"message": "Passwords must match."}
            )
        # Attempt to create new user, if user already exists ,raises integrity error
        try:
            # print(f"{name}\n {email}\n {contact}\n {alternate_contact}\n {password} and {confirmation}\n {dob}\n {gender}")
            user = User.objects.create_admin_doc(
                firstname=firstname,
                lastname= lastname, 
                email=email,
                password=password,          
                primary_contact=contact,
                alternate_contact=alternate_contact,
                user_id=user_id,
                gender = gender,
                dob=dob,
                address=address,
                )
            user.save()
        except IntegrityError:
            return render(
                request,
                "admin_doc/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("admin_doc:index"))
    else:
        return render(request, "admin_doc/register.html")