from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import *
app_name = "administrator"



urlpatterns  = [
    path('get-all-user/', GetUsers.as_view(), name="all_users"),
    path('get-all-employees/', GetEmployees.as_view(), name="all_employees"),
    path('get-orders/', GetOrders.as_view(), name="all_orders"),
    path('get-category/', GetCategories.as_view(), name="all_categories"),
    path('get-services/', GetServices.as_view(), name="all_services"),
]