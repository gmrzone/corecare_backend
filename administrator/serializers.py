from rest_framework.serializers import ModelSerializer
from account.models import CustomUser
from cart.models import Order
from api.serializers import TimeSince, CouponCodeSerializers, EmployeeCategorySerializer, ServiceSerializer, SubcategorySerializer
from cart.serializers import CalculateFullfillTime, OrderItemSerializer

class UserSerializerAdministrator(ModelSerializer):

    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)


    class Meta:

        model = CustomUser
        fields = ('id','number', 'username', 'email', 'last_login', 'first_name', 'last_name',"address_1", "address_2", "city", "state", "pincode", "verified",'is_employee', 'is_active', 'is_verified_employee', 'date_joined')



class OrderSerializerAdministrator(ModelSerializer):
    coupon = CouponCodeSerializers(read_only=False)
    category = EmployeeCategorySerializer(read_only=False)
    items = OrderItemSerializer(many=True, read_only=False)
    created = TimeSince(read_only=True)
    updated = TimeSince(read_only=True)
    fullfill_by = CalculateFullfillTime(read_only=False)
    user = UserSerializerAdministrator(read_only=False)
    class Meta:
        model = Order
        fields = ('id', 'category', 'items', 'user', 'receipt', 'razorpay_order_id', 'subtotal', 'tax', 'discount', 'total', 'coupon', 'paid', 'status', 'created', 'updated', 'fullfill_by')

class ServiceSerializerAdministrator(ServiceSerializer):
    subcategory = SubcategorySerializer(read_only=False)