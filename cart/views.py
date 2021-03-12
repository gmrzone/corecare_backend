from django.shortcuts import render
from api.models import Service
from cart.models import Cart
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from .errors import CategoryChange
# Create your views here.

@api_view(['POST'])
def add_service_to_cart(request):
    service_id = request.data['service_id']
    category = request.data['category']
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        data = {'status': 'error'}
    else:
        try:
            cart = Cart(request=request)
            cart.add(service, category) 
        except CategoryChange as e:
            data = {'status': 'category_change', "mssg": str(e)}
        else:
            data = request.session[settings.CART_SESSION_ID]
    return Response(data)


@api_view(['POST'])
def remove_service_from_cart(request):
    service_id = request.data['service_id']
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        data = {'status': 'error'}
    else:
        cart = Cart(request=request)
        cart.remove(service)
        data = request.session[settings.CART_SESSION_ID]
    return Response(data)

@api_view(['GET'])
def get_cart(request):
    cart = Cart(request=request).get_cart()
    return Response(cart)

@api_view(['GET'])
def get_basic_cart(request):
    cart = Cart(request=request)
    return Response(cart.get_basic_cart())

@api_view(['GET'])
def clear_cart(request):
    cart = Cart(request=request)
    cart.clear_Cart()
    return Response({'status': 'ok'})



