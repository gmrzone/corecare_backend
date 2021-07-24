from django.contrib.auth.hashers import make_password
from django.db import Error, transaction
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (ModelSerializer, StringRelatedField,
                                        ValidationError)
from rest_framework.views import exception_handler

from account.models import CustomUser
from api.models import CouponCode, Service, ServiceSubcategory
from api.serializers import ServiceSerializer, SubcategorySerializer, TimeSince
from blog.models import Comment
from blog.serializers import PostSerializer
from cart.models import Order, OrderItem
from cart.serializers import CalculateFullfillTime
from cart.utils import generate_order_receipt


class UserSerializerAdministrator(ModelSerializer):

    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)
    photo = serializers.ImageField(write_only=True, required=False, allow_empty_file=True)
    photo_url = SerializerMethodField('get_photo', read_only=True)

    class Meta:

        model = CustomUser
        fields = (
            "id",
            "number",
            "password",
            "username",
            "email",
            "photo",
            "photo_url",
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

    def get_photo(self, obj):
        return obj.photo.url

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = CustomUser(**validated_data)
        user.save()
        return user


class EmployeeSerializerAdministrator(ModelSerializer):
    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)
    employee_category_detail = SerializerMethodField("get_employee_category")
    photo = serializers.ImageField(write_only=True, required=False, allow_empty_file=True)
    photo_url = SerializerMethodField('get_photo', read_only=True)

    class Meta:

        model = CustomUser
        fields = (
            "id",
            "number",
            "password",
            "username",
            "email",
            "photo",
            "photo_url",
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
            "employee_category_detail",
            "date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_photo(self, obj):
        return obj.photo.url

    def get_employee_category(self, obj):
        return {"name": obj.employee_category.name, "slug": obj.employee_category.slug}

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

    items = OrderItemMinSerializer(many=True)
    created = TimeSince(read_only=True)
    updated = TimeSince(read_only=True)
    fullfill_by = CalculateFullfillTime(read_only=True)
    user_detail = SerializerMethodField("get_user_detail")

    class Meta:
        model = Order
        fields = (
            "id",
            "category",
            "items",
            "user",
            "user_detail",
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
        extra_kwargs = {"items": {"required": False}, "receipt": {"required": False}}

    def get_user_detail(self, obj):
        return {
            "name": f"{obj.user.first_name} {obj.user.last_name}",
            "number": obj.user.number,
        }

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        try:
            with transaction.atomic():
                instance = Order(**validated_data)
                receipt = generate_order_receipt(17, instance.user.id)
                instance.receipt = receipt
                instance.save()
                for item in items_data:
                    OrderItem.objects.create(order=instance, **item)
        except Error:
            raise ValidationError(
                "Something is wrong with the server please try again later."
            )
        return instance


class ServiceSubcategorySerializerAdmin(ModelSerializer):
    created = TimeSince(read_only=True)
    service_specialist_detail = SerializerMethodField(
        "get_specialist_name", read_only=True
    )
    icon_url = SerializerMethodField('get_icon', read_only=True)
    icon = serializers.ImageField(write_only=True, required=False, allow_empty_file=True)
    class Meta:
        model = ServiceSubcategory
        fields = (
            "id",
            "name",
            "slug",
            "icon_url",
            "icon",
            "created",
            "service_specialist",
            "service_specialist_detail",
        )


    def get_icon(self, obj):
        return obj.icon.url
    def get_specialist_name(self, obj):
        return {
            "slug": obj.service_specialist.slug,
            "name": obj.service_specialist.name,
        }


class ServiceSerializerAdministrator(ServiceSerializer):
    subcategory_name = SerializerMethodField('get_subcategory_name')
    icon_url = SerializerMethodField('get_icon', read_only=True)
    icon = serializers.ImageField(write_only=True, required=False, allow_empty_file=True)


    class Meta:
        model = Service
        fields = ('id', 'name', 'price', "active", 'created', 'description', 'subcategory', "subcategory_name", 'icon', 'icon_url')
        read_only_fields = ('created', 'active', 'subcategory_name')

    def get_icon(self, obj):
        return obj.icon.url

    def get_subcategory_name(self, obj):
        return obj.subcategory.name

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
