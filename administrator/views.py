from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import UserSerializerAdministrator
from account.models import CustomUser
# Create your views here.



class GetUsers(ListAPIView):
    serializer_class = UserSerializerAdministrator
    http_method_names = ['get']
    queryset = CustomUser.objects.all()



