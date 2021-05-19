from .models import Order, OrderItem
from rest_framework.serializers import ModelSerializer, Field
from api.serializers import CouponCodeSerializers, TimeSince
from api.serializers import ServiceSerializer, EmployeeCategorySerializer
from account.serializers import UserSerializer
from datetime import timedelta
import pytz
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
        local_timezone = pytz.timezone('Asia/Kolkata')
        local_time = value.astimezone(local_timezone)
        future_date = local_time + timedelta(days=3)
        future_day = self.make_ordinal(future_date.strftime('%d'))
        date = future_date.strftime('%B-%Y %I:%M %p')
        return f"{future_day} {date}"


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
    coupon = CouponCodeSerializers(read_only=True)
    category = EmployeeCategorySerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    created = TimeSince(read_only=True)
    updated = TimeSince(read_only=True)
    fullfill_by = CalculateFullfillTime(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'category', 'items', 'user', 'receipt', 'razorpay_order_id', 'subtotal', 'discount', 'total', 'coupon', 'paid', 'status', 'created', 'updated', 'fullfill_by')