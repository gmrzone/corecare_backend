from .models import Order, OrderItem
from rest_framework.serializers import ModelSerializer, Field
from api.serializers import CouponCodeSerializers, TimeSince
from api.serializers import ServiceSerializer, EmployeeCategorySerializer
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
        # future_day = self.make_ordinal(datetime.strptime(value, "%d"))
        # future_month = self.select_month(datetime.strptime(value, "%m"))
        # future_year = datetime.strptime(value, "%Y")
        # future_hour = datetime.strptime(value, "%h")
        future_day = self.make_ordinal(value.strftime('%d'))
        future_month = self.select_month(value.strftime('%m'))
        future_year = value.strftime('%Y')
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
    class Meta:
        model = Order
        fields = ('category', 'items', 'user', 'receipt', 'razorpay_order_id', 'subtotal', 'discount', 'total', 'coupon', 'paid', 'status', 'created', 'updated', 'fullfill_by')