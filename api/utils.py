import os
from django.utils.text import slugify


def EmployeeIconLocation(instance, filename):
    path = os.path.join('Employee Category', instance.number, filename)
    return path

def SubcategoryIconLocation(instance, filename):
    path = os.path.join('Service SubCategory Images', slugify(instance.name), filename)
    return path

def ServiceIconLocation(instance, filename):
    path = os.path.join('Service Images', slugify(instance.name), filename)
    return path
