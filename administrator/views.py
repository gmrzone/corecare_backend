from django.db.models import query
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import UserSerializerAdministrator, OrderSerializerAdministrator, ServiceSerializerAdministrator
from account.models import CustomUser
from cart.models import Order
from api.models import ServiceSubcategory, Service
from .permissions import IsSuperUser
from api.serializers import SubcategorySerializer, ServiceSerializer


# Create your views here.



class GetUsers(ListAPIView):
    serializer_class = UserSerializerAdministrator
    http_method_names = ['get']
    permission_classes = [IsSuperUser]
    queryset = CustomUser.objects.all()


class GetEmployees(ListAPIView):
    serializer_class = UserSerializerAdministrator
    permission_classes = [IsSuperUser]
    http_method_names = ['get']
    

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_employee=True)
        return queryset

class GetOrders(ListAPIView):
    serializer_class = OrderSerializerAdministrator
    permission_classes = [IsSuperUser]
    http_method_names = ['get']
    

    def get_queryset(self):
        queryset = Order.objects.all().select_related('category', 'user', 'coupon').prefetch_related('items', 'items__service', 'coupon__category')
        return queryset


class GetCategories(ListAPIView):
    serializer_class = SubcategorySerializer
    permission_classes = [IsSuperUser]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = ServiceSubcategory.objects.all().select_related('service_specialist')
        return queryset


class GetServices(ListAPIView):
    serializer_class = ServiceSerializerAdministrator
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Service.objects.all().select_related('subcategory', 'subcategory__service_specialist')
        return queryset
        






