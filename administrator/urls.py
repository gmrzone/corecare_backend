from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import GetUsers
app_name = "administrator"

@api_view(['GET'])
def test(request):
    return Response({})



urlpatterns  = [
    path('get_all_user/', GetUsers.as_view(), name="users")

]