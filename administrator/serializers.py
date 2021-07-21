from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, StringRelatedField
from account.models import CustomUser
from cart.models import Order
from api.serializers import TimeSince, CouponCodeSerializers, EmployeeCategorySerializer, ServiceSerializer, SubcategorySerializer
from cart.serializers import CalculateFullfillTime, OrderItemSerializer
from blog.models import Comment
from blog.serializers import PostSerializer
from api.models import CouponCode

class UserSerializerAdministrator(ModelSerializer):

    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)


    class Meta:

        model = CustomUser
        fields = ('id','number', 'username', 'email', 'last_login', 'first_name', 'last_name',"address_1", "address_2", "city", "state", "pincode", "verified",'is_employee', 'is_active', 'is_verified_employee', 'date_joined')



class OrderSerializerAdministrator(ModelSerializer):
    coupon = CouponCodeSerializers(read_only=True)
    category = EmployeeCategorySerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    created = TimeSince(read_only=True)
    updated = TimeSince(read_only=True)
    fullfill_by = CalculateFullfillTime(read_only=True)
    user = UserSerializerAdministrator(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'category', 'items', 'user', 'receipt', 'razorpay_order_id', 'subtotal', 'tax', 'discount', 'total', 'coupon', 'paid', 'status', 'created', 'updated', 'fullfill_by')

class ServiceSerializerAdministrator(ServiceSerializer):
    subcategory = SubcategorySerializer(read_only=False)


class BlogPostAdministrator(PostSerializer):
    author = StringRelatedField()


class CommentSerializerAdmin(ModelSerializer):
    created = TimeSince(read_only=True)
    user = StringRelatedField()


    class Meta:
        model = Comment
        fields = ("id", 'parent', 'user', 'name', "email", "replies", "comment", "active", "created")



class CouponSerializerAdministrator(ModelSerializer):
    users = StringRelatedField(many=True, read_only=True)
    valid_from = SerializerMethodField('get_valid_from')
    valid_to = SerializerMethodField('get_valid_to')
    category = StringRelatedField(read_only=True, many=True)
    class Meta:
        model = CouponCode
        fields = ('code', 'discount', 'valid_from', 'valid_to', 'active', 'category', 'users')

    def get_valid_from (self, obj):
        valid_from = obj.valid_from
        if not valid_from:
            return None
        return {
            "year": valid_from.year,
            "month": valid_from.month,
            "day": valid_from.day
        }

    def get_valid_to (self, obj):
        valid_to = obj.valid_to
        if not valid_to:
            return None
        return {
            "year": valid_to.year,
            "month": valid_to.month,
            "day": valid_to.day
        }