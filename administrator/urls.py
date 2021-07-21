from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import GetUsers, GetEmployees
app_name = "administrator"



urlpatterns  = [
    path('get_all_user/', GetUsers.as_view(), name="users"),
    path('get_all_employees/', GetEmployees.as_view(), name="employees"),

]