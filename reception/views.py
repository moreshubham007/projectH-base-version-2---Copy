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
#------------------------------
#      Utility Functions
from projectH import utils
#-------------------------------
#		  DB Models
#-----------------------------
#       User Model
from django.contrib.auth import get_user_model
User = get_user_model()
#-------------------------------
#       Schedule Model
from reception.models import Schedule,DaysOfTheWeek
#--------------------------------------
#		Appointment Model
from reception.models import Appointment
#--------------------------------------
#--------------------------------


def index(request):
	if request.user.is_authenticated and request.user.groups.filter(name="Receptionist").exists():
		return render(request,"reception/dashboard.html",{
			"doctor_list":User.objects.filter(is_as_doc=True),
			"patient_list":User.objects.filter(is_as_doc=False,is_admin_doc=False),
			"new_patient_count":len(User.objects.filter(is_as_doc=False,is_admin_doc=False,patient_type='N')),
			"existing_patient_count":len(User.objects.filter(is_as_doc=False,is_admin_doc=False,patient_type='E'))
		})
	else:
		if request.user.is_authenticated:
			logout(request)
		return render(request,"reception/index.html") 
		

def reception_login(request):
	if request.user.is_authenticated and user.groups.filter(name="Receptionist").exists():
		return render(request,"reception/dashboard.html")
	elif request.method == "GET":
		return HttpResponseRedirect(reverse("reception:index"))

	elif request.method == "POST":
		email = request.POST["email"]
		password = request.POST["pwd"]
		# users = User.objects.filter(is_admin_doc=True)

		users= User.objects.filter(email=email,is_admin_doc=True)
		if not users.exists():
			return render(request,"reception/index.html",
			{"message": "Invalid username and/or password."},)
		user = authenticate(email=email,password=password)

		if user.is_admin_doc and user.groups.filter(name="Receptionist").exists():
			login(request,user)
			return HttpResponseRedirect(reverse("reception:index"))
		return render(request,"reception/index.html",
			{"message": user.email + " does not have access, contact your admin."},)


def reception_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse("reception:index"))

# doctors
@login_required(login_url="login")
def show_doctors(request):
	#  get list of all doctors
	doctors = User.objects.filter(is_as_doc=True)
	if request.method=='GET':
		return render(request,"reception/doctors.html",
		{
			"doctors":doctors,
		})
	elif request.method=='POST':
		search_input = request.POST["searched_input"]
		search_input = search_input.upper()
		requested_doctor=[]
		for doctor in doctors:
			if (search_input in (doctor.firstname).upper()) or (search_input in (doctor.lastname).upper()):
				requested_doctor.append(doctor)
				print("found",doctor)
		return render(request,"reception/doctors.html",
		{
			"doctors":requested_doctor,
		})

@login_required(login_url="login")
def add_doctor(request):
	if request.method=='POST':
		firstname = request.POST["first_name"]
		lastname = request.POST["last_name"]
		email = request.POST["emailid"]
		dob = request.POST["dob"]
		emp_id = request.POST["employee_id"]
		gender = request.POST["gender"]
		contact = request.POST["phone"]
		alternate_contact = request.POST["alphone"]
		password = request.POST["password"]
		confirmation = request.POST["password"]
		status = request.POST["status"]
		address = ""

		# convert string to date format
		dob = utils.str_to_date(dob)

		# print(f"{firstname}\n {email}\n {contact}\n {alternate_contact}\n {password} and {confirmation}\n {dob}\n {gender}\n {status}\n")
		# return HttpResponse("Success")
		# Attempt to create new user, if user already exists ,raises integrity error
		try:
			user = User.objects.create_as_doc(
            firstname=firstname,
            lastname= lastname, 
            email=email,
            password=password,          
            primary_contact=contact,
            user_id=emp_id,
            alternate_contact=alternate_contact,
            gender = gender,
            dob=dob,
			address=address,
            )
			user.status = status
			user.save()
		except IntegrityError:
			return render(
                request,
                "reception/add-doctor.html",
                {"error": "Email already taken.",
				"emp_id":emp_id,},
            )
		id_list=[]
		while(True):
			emp_id =utils.empid_gen()
			id_list = User.objects.filter(user_id=emp_id)
			# if user id is unique then take it
			# otherwise generate user id again
			if(len(id_list)==0):
			    break
		return render(request,
			"reception/add-doctor.html",
			{"success":"Doctor added successfully",
			"emp_id":emp_id},)
	else:       
		# generate user id
		id_list=[]
		while(True):
			emp_id =utils.empid_gen()
			id_list = User.objects.filter(user_id=emp_id)
			# if user id is unique then take it
			# otherwise generate user id again
			if(len(id_list)==0):
			    break
		return render(request,"reception/add-doctor.html",
		{
			"emp_id":emp_id,
		},)

@login_required(login_url="login")
def edit_doctor(request,id):
	user = User.objects.get(user_id=id)
	if request.method=='GET':
		return render(request,
		"reception/edit-doctor.html",
		{
			"doctor":user,
			"dob":utils.date_to_string(user.dob),
		})
	elif request.method=='POST':
		firstname = request.POST["first_name"]
		lastname = request.POST["last_name"]
		email = request.POST["emailid"]
		dob = request.POST["dob"]
		contact = request.POST["phone"]
		alternate_contact = request.POST["alphone"]
		status = request.POST["status"]
		
		if (len(User.objects.filter(email=email))!=0) and (email != user.email):
			return render(request,
		"reception/edit-doctor.html",
		{
			"doctor":user,
			"dob":utils.date_to_string(user.dob),
			"error":"Email is taken by someone, Please give another mail."
		})

		# convert string to date format
		dob = utils.str_to_date(dob)

		user.firstname = firstname
		user.lastname = lastname
		user.email = email
		user.dob = dob
		user.primary_contact=contact
		user.alternate_contact=alternate_contact
		user.status = status
		user.save()
		return HttpResponseRedirect(reverse("reception:show_doctors"))

@login_required(login_url="login")
def delete_doctor(request,id):
	user = User.objects.get(user_id=id)
	user.delete()
	return HttpResponseRedirect(reverse("reception:show_doctors"))

@login_required(login_url="login")
def update_doctor_password(request,id):
	user = User.objects.get(user_id=id)
	if request.method=='GET':
		return render(request,
		"reception/update-password.html",
		{
			"email":user.email,
			"id":user.user_id,
		}
		)
	elif request.method=='POST':
		password = request.POST["pwd"]
		confirm_password = request.POST["cpwd"]
		
        # Ensure password matches confirm_password
		if not utils.validate_password(password,confirm_password):
			return render(request,
			"reception/update-password.html",
			{
				"email":user.email,
				"id":user.user_id,
				"message": "Passwords must match.",
			}
			)
		# if passwords are matched
		user.set_password(password)
		user.save()
		return HttpResponseRedirect(reverse("reception:show_doctors"))

# Patients
@login_required(login_url="login")
def show_patients(request):
	all_patient = User.objects.filter(is_as_doc=False,is_admin_doc=False)
	current_year = utils.get_year()
	
	if request.method  == 'GET':
		return render(request,
		"reception/patients.html",{
			# get all the list of patients
			"patients":all_patient,
			"current_year":current_year,
		})
	elif request.method  == 'POST':
		search_patient_input = request.POST["searched_patient"].upper()
		requested_patient=[]
		for patient in all_patient:
			# searched by name, id, phone number
			if (search_patient_input in (patient.firstname).upper()) or (search_patient_input in (patient.lastname).upper()) or (search_patient_input in (patient.user_id).upper()) or (search_patient_input in patient.primary_contact) or (search_patient_input in patient.alternate_contact):
				print("found ",patient)
				requested_patient.append(patient)
		return render(request,
		"reception/patients.html",{
			# get all the list of patients
			"patients":requested_patient,
			"current_year":current_year,
		}) 



@login_required(login_url="login")
def add_patient(request):
	if request.method == 'POST':
		firstname = request.POST["first_name"]
		lastname = request.POST["last_name"]
		email = request.POST["emailid"]
		dob = request.POST["dob"]
		gender = request.POST["gender"]
		contact = request.POST["phone"]
		alternate_contact = request.POST["aphone"]
		password = request.POST["password"]
		confirmation = request.POST["password"]
		patient_type = request.POST["patient_type"]
		address = request.POST["address"]

		dob = utils.str_to_date(dob)
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
		# print(f"{user_id}\n {firstname}\n {lastname}\n {email}\n {contact}\n {alternate_contact}\n {password} and {confirmation}\n {dob}\n {gender}\n {patient_type}")
		try:
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
                address=address,)
			user.patient_type=patient_type
			user.save()
			return render(request,
			"reception/add-patient.html",{
			"success":"Doctor added successfully",
		})
		except IntegrityError:
			return render(
                request,
                "reception/add-patient.html",
                {"error": "Email already taken."},
            )
	else:
		return render(request,
	"reception/add-patient.html")

@login_required(login_url="login")
def edit_patient(request,id):
	patient = User.objects.get(user_id=id)
	if request.method=='GET':
		return render(request,
		"reception/edit-patient.html",{
			"patient":patient,
			"dob":utils.date_to_string(patient.dob),
		})
	elif request.method=='POST':
		firstname = request.POST["first_name"]
		lastname = request.POST["last_name"]
		email = request.POST["emailid"]
		dob = request.POST["dob"]
		gender = request.POST["gender"]
		contact = request.POST["phone"]
		alternate_contact = request.POST["aphone"]
		patient_type = request.POST["patient_type"]
		address = request.POST["address"]

		dob = utils.str_to_date(dob)
		
		if (len(User.objects.filter(email=email))!=0) and (email != patient.email):
			return render(request,
			"reception/edit-patient.html",
		{
			"patient":patient,
			"dob":utils.date_to_string(patient.dob),
			"error":"Email is taken by someone, Please give another mail."
		})

		patient.firstname = firstname
		patient.lasttname = lastname
		patient.email = email
		patient.dob = dob
		patient.gender = gender
		patient.primary_contact = contact
		patient.alternate_contact = alternate_contact
		patient.patient_type = patient_type
		patient.address = address
		patient.save()
		return HttpResponseRedirect(reverse("reception:show_patients"))

@login_required(login_url="login")
def delete_patient(request,id):
	user = User.objects.get(user_id=id)
	user.delete()
	return HttpResponseRedirect(reverse("reception:show_patients"))

@login_required(login_url="login")
def update_patient_password(request,id):
	user = User.objects.get(user_id=id)
	if request.method=='GET':
		return render(request,
		"reception/update-password-patient.html",
		{
			"email":user.email,
			"id":user.user_id,
		}
		)
	elif request.method=='POST':
		password = request.POST["pwd"]
		confirm_password = request.POST["cpwd"]
		
        # Ensure password matches confirm_password
		if not utils.validate_password(password,confirm_password):
			return render(request,
			"reception/update-password-patient.html",
			{
				"email":user.email,
				"id":user.user_id,
				"message": "Passwords must match.",
			}
			)
		# if passwords are matched
		user.set_password(password)
		user.save()
		return HttpResponseRedirect(reverse("reception:show_patients"))

# Appointments
@login_required(login_url="login")
def show_appointments(request):
	all_appointments =Appointment.objects.all().exclude(status='D')
	current_year = utils.get_year()

	if request.method == 'GET':
		return render(request,
		"reception/appointments.html",{
		"appointments":all_appointments,
		"current_year":current_year,
	})
	elif request.method == 'POST':
		searched_appointment_query = request.POST["searched_appointment"].upper()
		searched_appointment=[]

		for appointment in all_appointments:
			if (searched_appointment_query in appointment.appointment_id) or (searched_appointment_query in (appointment.patient.firstname).upper()) or (searched_appointment_query in (appointment.patient.lastname).upper()):
				searched_appointment.append(appointment)
		return render(request,
		"reception/appointments.html",{
		"appointments":searched_appointment,
		"current_year":current_year,
	})	

@login_required(login_url="login")
def add_appointment(request):
	if request.method=='GET':
		while(True):
			new_appointment_id = utils.apt_gen() 
			existing_appointment_id = Appointment.objects.filter(appointment_id=new_appointment_id)
			if new_appointment_id!=existing_appointment_id:
				break
		return render(request,
	"reception/add-appointment.html",{
		"apt_id":new_appointment_id,
		"patients":User.objects.filter(is_admin_doc=False,is_as_doc=False),
		"doctors":User.objects.filter(is_as_doc=True),
	})
	elif request.method=='POST':
		appointment_id = request.POST["appointment_id"]
		patient_id = request.POST["patient_name"]
		doctor_id = request.POST["doctor_name"]
		date = request.POST["date"]
		time = request.POST["time"]
		message = request.POST["message"]
		status=request.POST["status"]

		# extract appointment_id from input value
		appointment_id = utils.extractApt_id(appointment_id)

		patient_info = User.objects.get(user_id=patient_id)
		doctor_info = User.objects.get(user_id=doctor_id)
		
		# convert string to date
		date = utils.str_to_date(date)
		# convert string to time
		time_full = utils.str_to_time(time)
		time = time_full[0]
		am_pm = time_full[1]


		print(f"{appointment_id}\n {patient_id}\n {doctor_id}\n {date}\n {time} \n {message}")
		Appointment.objects.create(
			appointment_id=appointment_id,
			patient=patient_info,
			doctor = doctor_info,
			date = date,
			time = time,
			am_pm = am_pm,
			message=message,
			status= status,
		)
		return HttpResponseRedirect(reverse("reception:show_appointments"))


@login_required(login_url="login")
def edit_appointment(request,appointment_id):
	appointment = Appointment.objects.get(appointment_id=appointment_id)
	if request.method=="GET":
		return render(request,
		"reception/edit-appointment.html",{
			"appointment":appointment,
			"patients":User.objects.filter(is_admin_doc=False,is_as_doc=False),
			"doctors":User.objects.filter(is_as_doc=True),
			"date":utils.date_to_string(appointment.date),
			"time":utils.time_to_str(appointment.time) +" "+ appointment.am_pm,
		})
	if request.method=="POST":
		appointment_id = request.POST["appointment_id"]
		patient_id = request.POST["patient_name"]
		doctor_id = request.POST["doctor_name"]
		date = request.POST["date"]
		time = request.POST["time"]
		message = request.POST["message"]
		status=request.POST["status"]

		# extract appointment_id from input value
		appointment_id = utils.extractApt_id(appointment_id)

		patient_info = User.objects.get(user_id=patient_id)
		doctor_info = User.objects.get(user_id=doctor_id)
		
		# convert string to date
		date = utils.str_to_date(date)
		# convert string to time
		time_full = utils.str_to_time(time)
		time = time_full[0]
		am_pm = time_full[1]

		appointment = Appointment.objects.get(appointment_id=appointment_id)
		appointment.appointment_id=appointment_id
		appointment.patient = patient_info
		appointment.doctor = doctor_info
		appointment.date = date
		appointment.time = time
		appointment.am_pm = am_pm
		appointment.message = message
		appointment.status = status


		# print(status)

		appointment.save()
		# return HttpResponse("Success")
		return HttpResponseRedirect(reverse("reception:show_appointments"))


@login_required(login_url="login")
def delete_appointment(request,appointment_id):
	appointment = Appointment.objects.get(appointment_id=appointment_id)
	appointment.delete()
	return HttpResponseRedirect(reverse("reception:show_appointments"))

@login_required(login_url="login")
def show_archive_appointments(request):
	# get all appointment with done status
	all_appointments =Appointment.objects.filter(status='D')
	current_year = utils.get_year()
	if request.method=='GET':
		return render(request,
		"reception/archive-appointments.html",{
		"appointments":all_appointments,
		"current_year":current_year,
	})
	elif request.method =='POST':
		searched_archived_query = request.POST["searched_archived_appointment"].upper()
		searched_archived_appoitment=[]
		for appointment in all_appointments:
			if (searched_archived_query in appointment.appointment_id) or (searched_archived_query in (appointment.patient.firstname).upper()) or (searched_archived_query in (appointment.patient.lastname).upper()):
				searched_archived_appoitment.append(appointment)
		return render(request,
			"reception/archive-appointments.html",{
			"appointments":searched_archived_appoitment,
			"current_year":current_year,
		})


@login_required(login_url="login")
def archive_appointment(request,appointment_id):
	appointment = Appointment.objects.get(appointment_id=appointment_id)
	# change to done/archive status
	appointment.status = 'D'
	appointment.save()
	return HttpResponseRedirect(reverse("reception:show_appointments"))

@login_required(login_url="login")
def unarchive_appointment(request,appointment_id):
	appointment = Appointment.objects.get(appointment_id=appointment_id)
	# change to confirmed appointment
	appointment.status = 'C'
	appointment.save()
	return HttpResponseRedirect(reverse("reception:show_appointments"))

@login_required(login_url="login")
def edit_archive_appointment(request,appointment_id):
	appointment = Appointment.objects.get(appointment_id=appointment_id)
	if request.method=='GET':
		return render(request,
		"reception/edit-archive-appointment.html",{
			"appointment":appointment,
			"date":utils.date_to_string(appointment.date),
			"time":utils.time_to_str(appointment.time) +" "+ appointment.am_pm,
		})
	elif request.method == 'POST':
		message = request.POST["message"]

		appointment.message = message
		appointment.save()
		return HttpResponseRedirect(reverse("reception:show_archive_appointments"))



@login_required(login_url="login")
def show_doctor_schedules(request):
	return render(request,
	"reception/schedule.html",{
		"schedules":Schedule.objects.all(),
	})

@login_required(login_url="login")
def add_doctor_schedule(request):
	if request.method == 'GET':
		return render(request,
		"reception/add-schedule.html",{
			"doctors":User.objects.filter(is_as_doc=True),
		})
	elif request.method =='POST':
		doctor_id = request.POST["doctor_name"]
		days = request.POST.getlist("days")
		from_time = request.POST["start_time"]
		to_time = request.POST["end_time"]
		message = request.POST["message"]

		doctor_info = User.objects.get(user_id=doctor_id)

		# one schedule per doctor validation
		if Schedule.objects.filter(doctor=doctor_info).exists():
			return render(
                request,
                "reception/add-schedule.html",
                {"error": "Schedule already exists, Please edit the existing schedule.",
							"doctors":User.objects.filter(is_as_doc=True),},
            )
		# print(request.POST)
		# print(days)
		# string to time
		from_time_full = utils.str_to_time(from_time)
		from_time = from_time_full[0]
		from_am_pm = from_time_full[1]

		# string to time
		to_time_full = utils.str_to_time(to_time)
		to_time = to_time_full[0]
		to_am_pm = to_time_full[1]

		new_schedule = Schedule()
		new_schedule.doctor=doctor_info
		new_schedule.available_time_from=from_time
		new_schedule.from_am_pm=from_am_pm
		new_schedule.available_time_to=to_time
		new_schedule.to_am_pm=to_am_pm
		new_schedule.message=message
		new_schedule.save()

		# add days one by one
		print(days)
		for day in days:
			a = DaysOfTheWeek.objects.get(available_days=day)
			new_schedule.working_days.add(a)


		return HttpResponseRedirect(reverse("reception:show_doctor_schedules"))
		# return HttpResponse("success")



@login_required(login_url="login")
def edit_doctor_schedule(request,id):
	schedule = Schedule.objects.get(id=id)

	week_days = set(DaysOfTheWeek.objects.all())
	scheduled_week_days = set(schedule.working_days.all())
	if request.method =='GET':
		return render(request,
		"reception/edit-schedule.html",
		{
			"schedule":schedule,
			"doctors":User.objects.filter(is_as_doc=True),
			"from_date": utils.time_to_str(schedule.available_time_from)+ schedule.from_am_pm,
			"to_date":utils.time_to_str(schedule.available_time_to)+schedule.to_am_pm,
			"other_week_days": week_days.symmetric_difference(scheduled_week_days),
		})
	elif request.method =='POST':
		doctor_id = request.POST["doctor_name"]
		days = request.POST.getlist("days")
		from_time = request.POST["start_time"]
		to_time = request.POST["end_time"]
		message = request.POST["message"]

		doctor_info = User.objects.get(user_id=doctor_id)

		# string to time
		from_time_full = utils.str_to_time(from_time)
		from_time = from_time_full[0]
		from_am_pm = from_time_full[1]

		# string to time
		to_time_full = utils.str_to_time(to_time)
		to_time = to_time_full[0]
		to_am_pm = to_time_full[1]

		# saving data in existing schedule
		schedule.doctor=doctor_info
		schedule.available_time_from=from_time
		schedule.from_am_pm=from_am_pm
		schedule.available_time_to=to_time
		schedule.to_am_pm=to_am_pm
		schedule.message=message
		schedule.save()

		# remove all existing days
		for existing_days in schedule.working_days.all():
			schedule.working_days.remove(existing_days)
		# add days one by one
		print(days)
		for day in days:
			a = DaysOfTheWeek.objects.get(available_days=day)
			schedule.working_days.add(a)
			# print("Added : ",a)
		
		schedule.save()


		return HttpResponseRedirect(reverse("reception:show_doctor_schedules"))



@login_required(login_url="login")
def delete_doctor_schedule(request,id):
	schedule = Schedule.objects.get(id=id)
	schedule.delete()

	return HttpResponseRedirect(reverse("reception:show_doctor_schedules"))


