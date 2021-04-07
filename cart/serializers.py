from .models import Order, OrderItem
from rest_framework.serializers import ModelSerializer, Field
from api.serializers import CouponCodeSerializers, TimeSince
from api.serializers import ServiceSerializer, EmployeeCategorySerializer
from account.serializers import UserSerializer
from datetime import timedelta
# class date(Field):
#     def to_representation(self, value):
#         return timesince(value) + " ago"
class OrderItemSerializer(ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = OrderItem
        fields = ['service', 'quantity', 'total']

class CalculateFullfillTime(Field):
    def __init__(self, *args, **kwargs):
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        future_date = value + timedelta(days=3)
        future_day = self.make_ordinal(future_date.strftime('%d'))
        future_month = self.select_month(future_date.strftime('%m'))
        future_year = future_date.strftime('%Y')
        return f"{future_day} {future_month} {future_year}"


    def make_ordinal(self, number):
        number = int(number)
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(number % 10, 4)]
        if 11 <= (number % 100) <= 13:
            suffix = 'th'
        return str(number) + suffix

    def select_month(self, number):
        index = int(number) - 1
        return self.months[index]

        

class OrderSerializer(ModelSerializer):
    coupon = CouponCodeSerializers(many=False)
    category = EmployeeCategorySerializer()
    items = OrderItemSerializer(many=True)
    created = TimeSince()
    updated = TimeSince()
    fullfill_by = CalculateFullfillTime()
    user = UserSerializer()
    class Meta:
        model = Order
        fields = ('id', 'category', 'items', 'user', 'receipt', 'razorpay_order_id', 'subtotal', 'discount', 'total', 'coupon', 'paid', 'status', 'created', 'updated', 'fullfill_by')