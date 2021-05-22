# Django Imports
from api.serializers import ServiceSerializer
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.template.loader import render_to_string
from django.http import HttpResponse

# Project Import
from api.models import CouponCode, EmployeeCategory, Service
from cart.models import Cart
from .errors import CategoryChange
from string import ascii_lowercase, ascii_uppercase
from .models import Order, OrderItem
from .utils import Recommender
from .serializers import OrderSerializer
from .tasks import order_success_mail
# Other Modules Imports
from datetime import datetime
import razorpay
import weasyprint

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

# Create your views here.
client = razorpay.Client(auth=('rzp_test_Fz30Ps4aOA4Zke', 'HS7mZz3v6G9dLeaS5LY1tejl'))

class AddServiceToCart(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
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

class RemoveServiceFromCart(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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

class DeleteService(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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


class CreateRazorPayOrder(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if user.address_1 and user.address_2 and user.city and user.state and user.pincode:
            cart = Cart(request)
            # client = razorpay.Client(auth=('rzp_test_Fz30Ps4aOA4Zke', 'HS7mZz3v6G9dLeaS5LY1tejl'))
            order_amount = cart.get_discounted_total()[0]
            order_currency = "INR"
            allowed_characters = datetime.now().strftime('%Y%m%d%H%M%S') + ascii_uppercase + ascii_lowercase
            order_receipt = 'ORD' + str(user.id) + get_random_string(17, allowed_characters)
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
        create_recommandation_list = []
        for i in cart.values():
            create_recommandation_list.append(i['service']['id'])
            service = cache.get(f"service_{i['service']['id']}")
            if not service:
                service = Service.objects.get(id=i.service.id)
            OrderItem.objects.create(order=order, service=service, quantity=i['quantity'], total=int(i['quantity']) * float(i['price']))
        
        Recommender().create_recommandation_for(create_recommandation_list)
        # Get basic Recommandation based on order to send via email via celery
        service_recommandation = Recommender().get_basic_recommandation(create_recommandation_list, max_result=4)
        order_success_mail.delay(cart_detail['order_receipt'], service_recommandation)
        # Clear Cart
        cartObject.clear_Cart()
        data = {'status': 'ok', 'msg': f"Paymant sucessfull your order with order id {order.receipt} has been created ", 'receipt': order.receipt}   
    return Response(data)


class CreateOrder(CreateAPIView):
    serializer_class = OrderSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        cart_obj = Cart(request)
        whole_cart = cart_obj.get_cart()
        cart_detail = whole_cart['cart_detail']
        cart = whole_cart['cart']
        serializer_data = {
            'razorpay_order_id': cart_detail['razorpay_order_id'],
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        try:
            p = client.utility.verify_payment_signature(serializer_data)
        except:
            data = {'status': 'error', 'msg': 'Payment signature could not be verified'}
        else:
            user = request.user
            coupon_id = cart_detail.get('coupon_id', False)
            coupon = CouponCode.objects.get(id=coupon_id) if coupon_id else None
            category = get_object_or_404(EmployeeCategory, slug=cart_detail['category'])
            receipt = cart_detail['order_receipt']
            serializer_data.update({'receipt': receipt,
                                    "subtotal": cart_detail['cart_subtotal'],
                                    "discount":cart_detail['discount'], 
                                    "total":cart_detail['total'],
                                    "paid":True
                                    })
            serializer = self.serializer_class(data=serializer_data)
            if serializer.is_valid():
                instance = serializer.save(user=user, coupon=coupon, category=category)
                create_recommandation_list = []
                for i in cart.values():
                    create_recommandation_list.append(i['service']['id'])
                    service = cache.get(f"service_{i['service']['id']}")
                    if not service:
                        service = Service.objects.get(id=i.service.id)
                        cache.set(f"service_{i['service']['id']}", service)
                    OrderItem.objects.create(order=instance, service=service, quantity=i['quantity'], total=int(i['quantity']) * float(i['price']))
                Recommender().create_recommandation_for(create_recommandation_list)
                cart_obj.clear_Cart()
                data = {'status': 'ok', 'msg': f"Paymant sucessfull your order with order id {receipt} has been created ", 'receipt': receipt}
            else:
                data = serializer.errors
            return Response(data)


        

@api_view(['GET'])
def get_basic_recommandation(request):
    cart = Cart(request)
    recommender = Recommender()
    recommandation_for = [id for id in cart.get_basic_cart().keys()]
    if len(recommandation_for) > 0:
        data = recommender.get_basic_recommandation(recommandation_for, max_result=7)
    else:
        data = []
    return Response(data)

@api_view(['GET'])
def get_detailed_recommandation(request):
    cart = Cart(request)
    recommender = Recommender()
    recommandation_for = [id for id in cart.get_basic_cart().keys()]
    if len(recommandation_for) > 0:
        data = recommender.get_detail_recommandation(recommandation_for, max_result=7)
    else:
        data = []
    return Response(data)

@api_view(['POST'])
def add_from_recommanded_toCart(request):
    service_id = request.data.get('service_id')
    category = request.data.get('category')
    if service_id and category:
        service = cache.get(f"service_{service_id}")
        if not service:
            service = Service.objects.get(pk=service_id)
            cache.set(f"service_{service_id}", service)
        cart = Cart(request=request)
        recommander = Recommender()
        cart.add(service, category=category)
        get_recommandation_for = [id for id in cart.get_basic_cart().keys()]
        if len(get_recommandation_for) > 0:
            rec = recommander.get_detail_recommandation(get_recommandation_for, max_result=7)
        else:
            rec = []
        added_service = ServiceSerializer(service).data
        added_service = {service_id: {
            'quantity': 1,
            'service': added_service,
            'price': added_service['price'],
            'total': added_service['price'],
            'added': True,
        }}
        cart_detail = cart.cart_detail
        cart_detail['cart_subtotal'] = str(cart.get_cart_total())
        cart_detail['total'], cart_detail['discount'] = cart.get_discounted_total()
        data = {'status': 'ok', 'added': added_service, "recommandedServices": rec, "cart_detail": cart_detail}
    else:
        data = {'status': 'error'}
    return Response(data)

def download_pdf(request, order_id):
    order = get_object_or_404(Order, receipt=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachments; filename=invoice_corecare_' + order_id
    pdf_str = render_to_string('invoice/invoice.html', {'order': order})
    stylesheet = [weasyprint.CSS(settings.BASE_DIR / "staticfiles/static/css/main.css")]
    weasyprint.HTML(string=pdf_str).write_pdf(response, stylesheets=stylesheet)
    return response
    









