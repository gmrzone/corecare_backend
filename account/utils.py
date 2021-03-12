import os
def employee_document_location(instance, filename):
    path = os.path.join("Employee_Documents", instance.number, filename)
    return path

def profile_pic_loc(instance, filename):
    path = os.path.join("Users_Profile_pic", instance.number, filename)
    return path