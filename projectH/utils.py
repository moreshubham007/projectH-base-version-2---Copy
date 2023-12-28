# matching two password
def validate_password(password,confim_password):
    if password==confim_password:
        return True
    else:
        return False

from string import digits,ascii_uppercase
from random import choice
from datetime import datetime
# user id generator
# format : XXXXXXYYYY
def uid_gen():
    yyyy = datetime.now().year
    id = "".join(choice(digits+ascii_uppercase) for i in range(6)) + str(yyyy)
    return str(id)

def empid_gen():
    id = "".join(choice(digits+ascii_uppercase) for i in range(6))
    return str(id)

def str_to_date(date_str):
    # date_str format dd-mm-yyyy
    date_object = datetime.strptime(date_str, '%d/%m/%Y').date()
    return date_object

def date_to_string(date):
    string_object = date.strftime("%d/%m/%Y")
    return string_object

# get age by entering dob
def get_year():
    return datetime.now().year

# generate appointment id
def apt_gen():
    id = "".join(choice(digits+ascii_uppercase) for i in range(4))
    return str(id)

# extract appointment id from input value
# input value = APT-0000
def extractApt_id(id):
    appointment_id = id.split("-")
    return appointment_id[1]

# convert string to time
def str_to_time(time_str):
# '%I:%M %p' = HH:MM AM/PM
    time_object = datetime.strptime(time_str, '%I:%M %p').time()
    am_pm_indicator = time_object.strftime('%p')
    return [time_object,am_pm_indicator]

# convert time to string
def time_to_str(time_obj):
    string_time = time_obj.strftime('%I:%M')
    return string_time