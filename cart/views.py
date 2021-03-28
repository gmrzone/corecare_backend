from django.shortcuts import get_object_or_404, render
from rest_framework import serializers
from api.models import CouponCode, EmployeeCategory, Service
from cart.models import Cart
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from .errors import CategoryChange
import razorpay
from django.utils.crypto import get_random_string
from datetime import datetime
from string import ascii_lowercase, ascii_uppercase
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from django.core.cache import cache
from rest_framework.viewsets import ViewSet
from .serializers import OrderSerializer
# Create your views here.
client = razorpay.Client(auth=('rzp_test_Fz30Ps4aOA4Zke', 'HS7mZz3v6G9dLeaS5LY1tejl'))
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

@api_view(['POST'])
def delete_service(request):
    service_id = request.data.get('service_id')
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        data = {'status': 'error'}
    else:
        cart = Cart(request=request)
        cart.delete_service(service)
        data = cart.get_basic_cart()
    return Response(data)

@api_view(['POST'])
def apply_Coupon(request):
    coupon_code = request.data.get('coupon_code')
    cart = Cart(request=request)
    data = cart.validate_coupon(coupon_code)
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_razorPay_order(request):
    user = request.user
    if user.address_1 and user.address_2 and user.city and user.state and user.pincode:
        cart = Cart(request)
        # client = razorpay.Client(auth=('rzp_test_Fz30Ps4aOA4Zke', 'HS7mZz3v6G9dLeaS5LY1tejl'))
        order_amount = cart.get_discounted_total()[0]
        order_currency = "INR"
        allowed_characters = datetime.now().strftime('%Y%m%d%H%M%S') + ascii_uppercase + ascii_lowercase
        order_receipt = 'ORD' + str(user.id) + get_random_string(16, allowed_characters)
        shipping_address = f"{user.address_1} {user.address_2} {user.city} {user.state} {user.pincode}"
        notes = {'shipping address': shipping_address}
        order = client.order.create({'amount': float(order_amount) * 100, 'currency': order_currency, 'receipt': order_receipt, 'notes': notes})
        if order['status'] == 'created':
            cart.razorpay_order_created(order['id'], order_receipt)
        data = {'status': 'ok', "receipt": order_receipt, 'order_details': order, 'user': {'name': f"{user.first_name} {user.last_name}", 'email': user.email, 'number': user.number}, 'notes': notes['shipping address']}
    else:
        data = {'status': 'error', 'msg': 'address_error'}
    return Response(data)

def create_order_helper(request, cart, cart_detail, razorpay_payment_id, razorpay_signature):
        user = request.user
        coupon_id = cart_detail.get('coupon_id')
        if coupon_id:
            coupon = CouponCode.objects.get(id=coupon_id)
        else:
            coupon = None
        category = get_object_or_404(EmployeeCategory, slug=cart_detail['category'])
        
        order, created = Order.objects.get_or_create(
            category=category, user=user, 
            receipt=cart_detail['order_receipt'], 
            razorpay_order_id=cart_detail['razorpay_order_id'],
            razorpay_payment_id = razorpay_payment_id,
            razorpay_signature = razorpay_signature,
            subtotal=cart_detail['cart_subtotal'],
            discount=cart_detail['discount'], total=cart_detail['total'],
            coupon=coupon,
            paid=True
            )
        for i in cart.values():
            service = cache.get(f"service_{i['service']['id']}")
            if not service:
                service = Service.objects.get(id=i.service.id)
            OrderItem.objects.create(order=order, service=service, quantity=i['quantity'], total=int(i['quantity']) * float(i['price']))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    # request body data
    razorpay_payment_id = request.data.get('razorpay_payment_id')
    razorpay_signature = request.data.get('razorpay_signature')
    # Session cart Object
    cartObject = Cart(request)
    user_cart = cartObject.get_cart()
    cart_detail = user_cart['cart_detail']
    cart = user_cart['cart']
    checkout_params = {'razorpay_order_id': cart_detail['razorpay_order_id'], 'razorpay_payment_id': razorpay_payment_id, 'razorpay_signature': razorpay_signature}
    try:
        p = client.utility.verify_payment_signature(checkout_params)
    except:
        data = {'status': 'error', 'msg': 'Payment signature could not be verified'}
    else:
        user = request.user
        coupon_id = cart_detail.get('coupon_id')
        if coupon_id:
            coupon = CouponCode.objects.get(id=coupon_id)
        else:
            coupon = None
        category = get_object_or_404(EmployeeCategory, slug=cart_detail['category'])
        
        order, created = Order.objects.get_or_create(
            category=category, user=user, 
            receipt=cart_detail['order_receipt'], 
            razorpay_order_id=cart_detail['razorpay_order_id'],
            razorpay_payment_id = razorpay_payment_id,
            razorpay_signature = razorpay_signature,
            subtotal=cart_detail['cart_subtotal'],
            discount=cart_detail['discount'], total=cart_detail['total'],
            coupon=coupon,
            paid=True
            )
        for i in cart.values():
            service = cache.get(f"service_{i['service']['id']}")
            if not service:
                service = Service.objects.get(id=i.service.id)
            OrderItem.objects.create(order=order, service=service, quantity=i['quantity'], total=int(i['quantity']) * float(i['price']))
        cartObject.clear_Cart()
        data = {'status': 'ok', 'msg': f"Paymant sucessfull your order with order id {order.receipt} has been created ", 'receipt': order.receipt}   
    return Response(data)


class OrderViewSet(ViewSet):
    
    def list(self, request):
        queryset = Order.objects.all().prefetch_related('items').select_related('coupon')
        ser = OrderSerializer(queryset, many=True)
        return Response(ser.data)

    def retrieve(self, request, pk):
        queryset = Order.objects.all().prefetch_related('items').select_related('coupon')
        order = get_object_or_404(queryset, receipt=pk)
        ser = OrderSerializer(order)
        return Response(ser.data)





