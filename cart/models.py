from api.models import Service
from django.db import models
from django.conf import settings
from decimal import Decimal
from api.serializers import ServiceSerializer
from .errors import CategoryChange

# Create your models here.
class Cart:
    def __init__(self, request) -> None:
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        category = self.session.get('category')
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        if not category:
            category = self.session['category'] = {}
        self.cart = cart
        self.category = category


    def save(self):
        self.session.modified = True

    def add(self, service, category, quantity=1):
        service_id = str(service.id)
        current_category = self.category.get('name', False)
        if not current_category or self.category.get('name',False) == category:
            if service_id in self.cart:
                self.cart[service_id]['quantity'] += 1
            else:
                self.cart[service_id] = {'quantity': quantity, "price": str(service.price)}
            self.category['name'] = category
            self.save()
        else:
            raise CategoryChange(f"Category Changed From {self.category['name'].capitalize()} to {category.capitalize()}")

        
    def remove(self, service, quantity=1):
        service_id = str(service.id)
        if service_id in self.cart:
            if self.cart[service_id]['quantity'] > 1:
                self.cart[service_id]['quantity'] -= quantity
            else:
                del self.cart[service_id]
            if not bool(self.cart):
               del self.session['category']
            self.save()
    
    def delete_service(self, service):
        service_id = str(service.id)
        if service_id in self.cart:
            del self.cart[service_id]
            self.save()

    def get_service_total(self, service_id):
        if service_id in self.cart:
            return self.cart[service_id]['quantity'] * Decimal(self.cart[service_id]['price'])

    def get_cart_total(self):
        return sum(item['quantity'] * Decimal(item['price']) for item in self.cart.values())

    def clear_Cart(self):
        del self.session[settings.CART_SESSION_ID]
        del self.session['category']
        self.save()

    def get_cart(self):
        cart = self.cart.copy()
        for key in cart.keys():
            service = Service.objects.get(id=key)
            cart[key]['service'] = ServiceSerializer(service).data
            cart[key]['total'] = self.get_service_total(key)
        return cart
    def get_basic_cart(self):
        return self.cart

