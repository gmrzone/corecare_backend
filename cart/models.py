
from django.db.models.aggregates import Max
from django.db.models.fields import DateTimeField
from api.models import EmployeeCategory, Service
from django.db import models
from django.conf import settings
from decimal import Decimal
from api.serializers import ServiceSerializer
from .errors import CategoryChange
from django.utils import timezone
from api.models import CouponCode
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from api.models import Service
from django.conf import settings
from django.core.cache import cache
from datetime import timedelta
from django.utils import timezone
# Create your models here.
class Cart:
    def __init__(self, request) -> None:
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        cart_detail = self.session.get('cart_detail')
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        if not cart_detail:
            cart_detail = self.session['cart_detail'] = {}
        self.cart = cart
        self.cart_detail = cart_detail
       


    def save(self):
        self.session.modified = True

    def add(self, service, category, quantity=1):
        service_id = str(service.id)
        current_category = self.cart_detail.get('category', False)
        if not current_category or current_category == category:
            if service_id in self.cart:
                self.cart[service_id]['quantity'] += 1
            else:
                self.cart[service_id] = {'quantity': quantity, "price": str(service.price)}
            self.cart_detail['category'] = category
            self.save()
        else:
            raise CategoryChange(f"Category Changed From {self.cart_detail['category'].capitalize()} to {category.capitalize()}")

        
    def remove(self, service, quantity=1):
        service_id = str(service.id)
        if service_id in self.cart:
            if self.cart[service_id]['quantity'] > 1:
                self.cart[service_id]['quantity'] -= quantity
            else:
                del self.cart[service_id]
                if not bool(self.cart):
                    del self.session['cart_detail']
            self.save()
    
    def delete_service(self, service):
        service_id = str(service.id)
        if service_id in self.cart:
            del self.cart[service_id]
            if not bool(self.cart):
                del self.session['cart_detail']
            self.save()

    def validate_coupon(self, coupon_code):
        now = timezone.now()
        try:
            coupon = CouponCode.objects.get(code=coupon_code, valid_from__lte=now, valid_to__gte=now)
        except CouponCode.DoesNotExist:
            data = {'status': "invalid_coupon", 'msg': f"{coupon_code} is not a valid Coupon Code"}
        else:
            if coupon.category.all():
                if not coupon.category.filter(slug=self.cart_detail['category']).exists():
                    data = {'status': 'category_error', 'msg': f'{coupon_code} is not applicable for current category'}
                else:
                    data = self.apply_coupon(coupon_code, coupon)
            else:
                data = self.apply_coupon(coupon_code, coupon)
        return data

    def apply_coupon(self, coupon_code, coupon):
        self.cart_detail['coupon'] = coupon_code
        self.cart_detail['discount_percent'] = coupon.discount
        self.cart_detail['coupon_id'] = coupon.id
        self.save()
        data = self.get_cart()
        return data

    def get_service_total(self, service_id):
        if service_id in self.cart:
            return self.cart[service_id]['quantity'] * Decimal(self.cart[service_id]['price'])

    def get_cart_total(self):
        return sum(item['quantity'] * Decimal(item['price']) for item in self.cart.values())

    def get_cart_discount(self):
        pass
    
    def get_discounted_total(self):
        total = self.get_cart_total()
        discount_percent = self.cart_detail.get('discount_percent') or 0
        discount_amount = total * discount_percent / 100
        discounted_total = total - discount_amount
        return str(discounted_total),  str(discount_amount)

    def clear_Cart(self):
        del self.session[settings.CART_SESSION_ID]
        del self.session['cart_detail']
        self.save()
    
    def razorpay_order_created(self, razorpay_id, order_receipt):
        self.cart_detail['razorpay_order_id'] = razorpay_id
        self.cart_detail['order_receipt'] = order_receipt
        self.save()

    def get_cart(self):
        cart = self.cart.copy()
        cart_detail = self.cart_detail.copy()
        cart_detail['cart_subtotal'] = str(self.get_cart_total())
        cart_detail['total'], cart_detail['discount'] = self.get_discounted_total()
        for key in cart.keys():
            service = cache.get(f"service_{key}")
            if not service:
                service = Service.objects.get(id=key)
                cache.set(f"service_{key}", service)
            cart[key]['service'] = ServiceSerializer(service).data
            cart[key]['total'] = str(self.get_service_total(key))
        return {'cart': cart, 'cart_detail': cart_detail}
        
    def get_basic_cart(self):
        return self.cart


class Order(models.Model):
    FULLFILLED_BY = timezone.now() + timedelta(days=3)
    STATUS_CHOISES = (('pending', 'Pending'), ('processing', 'Processing'),('ongoing', 'OnGoing'),('cancelled', 'Cancelled'),('failed', 'Failed'),('completed', 'Completed'))
    category = models.ForeignKey(EmployeeCategory, on_delete=models.CASCADE, related_name="related_orders", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    receipt = models.CharField(max_length=100, db_index=True)
    razorpay_order_id = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=300, db_index=True, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(CouponCode, null=True, blank=True, on_delete=models.SET_NULL, related_name="related_orders")
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOISES, default="pending", max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fullfill_by = DateTimeField(default=FULLFILLED_BY)

    class Meta:
        ordering = ('-created',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service.name



