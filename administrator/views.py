from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import UserSerializerAdministrator
from account.models import CustomUser
from rest_framework.permissions import IsAdminUser

# Create your views here.



class GetUsers(ListAPIView):
    serializer_class = UserSerializerAdministrator
    http_method_names = ['get']
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()


class GetEmployees(ListAPIView):
    serializer_class = UserSerializerAdministrator
    permission_classes = [IsAdminUser]
    http_method_names = ['get']
    

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_employee=True)
        return queryset





