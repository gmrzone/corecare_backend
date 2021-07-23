from django.contrib.auth.hashers import make_password
from django.db import models
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, StringRelatedField, ValidationError

from account.models import CustomUser
from api.models import CouponCode
from api.serializers import (CouponCodeSerializers, EmployeeCategorySerializer,
                             ServiceSerializer, SubcategorySerializer,
                             TimeSince)
from blog.models import Comment
from blog.serializers import PostSerializer
from cart.models import Order, OrderItem
from cart.serializers import CalculateFullfillTime, OrderItemSerializer

from django.db import transaction, Error
class UserSerializerAdministrator(ModelSerializer):

    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)

    class Meta:

        model = CustomUser
        fields = (
            "id",
            "number",
            "password",
            "username",
            "email",
            "last_login",
            "first_name",
            "last_name",
            "address_1",
            "address_2",
            "city",
            "state",
            "pincode",
            "verified",
            "is_employee",
            "is_active",
            "date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = CustomUser(**validated_data)
        user.save()
        return user


class EmployeeSerializerAdministrator(ModelSerializer):
    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)
    extra_kwargs = {"password": {"write_only": True}}

    class Meta:

        model = CustomUser
        fields = (
            "id",
            "number",
            "password",
            "username",
            "email",
            "last_login",
            "first_name",
            "last_name",
            "address_1",
            "address_2",
            "city",
            "state",
            "pincode",
            "is_verified_employee",
            "is_employee",
            "is_active",
            "employee_category",
            "date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = CustomUser(**validated_data)
        user.save()
        return user

class OrderItemMinSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ("service", "quantity", "total")


class OrderSerializerAdministrator(ModelSerializer):
    # coupon = CouponCodeSerializers(read_only=True)
    # category = EmployeeCategorySerializer(read_only=True)
    items = OrderItemMinSerializer(many=True)
    created = TimeSince(read_only=True)
    updated = TimeSince(read_only=True)
    fullfill_by = CalculateFullfillTime(read_only=True)
    # user = UserSerializerAdministrator(read_only=True)
    class Meta:
        model = Order
        fields = (
            "id",
            "category",
            "items",
            "user",
            "receipt",
            "razorpay_order_id",
            "subtotal",
            "tax",
            "discount",
            "total",
            "coupon",
            "paid",
            "status",
            "created",
            "updated",
            "fullfill_by",
        )
        extra_kwargs = {'items': {'required': False}}

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        try:
            with transaction.atomic():
                instance = Order.objects.create(**validated_data)
                for item in items_data:
                    OrderItem.objects.create(order=instance, **item)
        except Error:
            raise ValidationError("Something is wrong with the server please try again later.")
        return instance
    


class ServiceSerializerAdministrator(ServiceSerializer):
    subcategory = SubcategorySerializer(read_only=False)


class BlogPostAdministrator(PostSerializer):
    author = StringRelatedField()


class CommentSerializerAdmin(ModelSerializer):
    created = TimeSince(read_only=True)
    user = StringRelatedField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "parent",
            "user",
            "name",
            "email",
            "replies",
            "comment",
            "active",
            "created",
        )


class CouponSerializerAdministrator(ModelSerializer):
    users = StringRelatedField(many=True, read_only=True)
    valid_from = SerializerMethodField("get_valid_from")
    valid_to = SerializerMethodField("get_valid_to")
    category = StringRelatedField(read_only=True, many=True)

    class Meta:
        model = CouponCode
        fields = (
            "code",
            "discount",
            "valid_from",
            "valid_to",
            "active",
            "category",
            "users",
        )

    def get_valid_from(self, obj):
        valid_from = obj.valid_from
        if not valid_from:
            return None
        return {
            "year": valid_from.year,
            "month": valid_from.month,
            "day": valid_from.day,
        }

    def get_valid_to(self, obj):
        valid_to = obj.valid_to
        if not valid_to:
            return None
        return {"year": valid_to.year, "month": valid_to.month, "day": valid_to.day}
