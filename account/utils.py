import os
from datetime import datetime
def employee_document_location(instance, filename):
    path = os.path.join("Employee_Documents", instance.number, filename)
    return path

def profile_pic_loc(instance, filename):
    path = os.path.join("Users_Profile_pic", instance.number, filename)
    return path

def validate_number(number):
    if number:
        return True
    else:
        return False
    

def generate_key_for_otp(number):
    return str(number) + str(datetime.date(datetime.now())) + "corecareservices"