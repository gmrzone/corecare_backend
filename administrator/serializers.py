from datetime import datetime

import pytz
from django.contrib.auth.hashers import make_password
from django.db import Error, transaction
from django.db.models import F
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (DateField, ImageField, ModelSerializer,
                                        ValidationError)

from account.models import CustomUser
from api.models import CouponCode, Service, ServiceSubcategory
from api.serializers import ServiceSerializer, SubcategorySerializer, TimeSince
from blog.models import Comment, Post
from cart.models import Order, OrderItem
from cart.serializers import CalculateFullfillTime
from cart.utils import generate_order_receipt


class UserSerializerAdministrator(ModelSerializer):

    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)
    photo = ImageField(write_only=True, required=False, allow_empty_file=True)
    photo_url = SerializerMethodField("get_photo", read_only=True)

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

    def update(self, instance, validated_data):
        if validated_data.get("password", None):
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class EmployeeSerializerAdministrator(ModelSerializer):
    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)
    employee_category_detail = SerializerMethodField("get_employee_category")
    photo = ImageField(write_only=True, required=False, allow_empty_file=True)
    photo_url = SerializerMethodField("get_photo", read_only=True)

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

    def update(self, instance, validated_data):
        if validated_data.get("password", None):
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


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
                items = (OrderItem(order=instance, **rest) for rest in items_data)
                OrderItem.objects.bulk_create(items)
        except Error:
            raise ValidationError(
                "Something is wrong with the server please try again later."
            )
        return instance

    def update(self, instance, validated_data):
        items_data = validated_data.get("items", None)
        if items_data:
            validated_data.pop("items")

            for item in items_data:
                obj, created = OrderItem.objects.get_or_create(**item, order=instance)
                if created:
                    instance.total = F("total") + (
                        item["total"]
                        * (100 - (F("discount") * 100 / F("subtotal")))
                        / 100
                    )
                    instance.subtotal = F("subtotal") + item["total"]
                    instance.discount = F("discount") + (
                        item["total"]
                        * (100 - (F("discount") * 100 / F("subtotal")))
                        / 100
                    )
                    instance.tax = F("tax") + (item["total"] * 5 / 100)
                    instance.save()
        else:
            instance.update(**validated_data)
        return instance


class ServiceSubcategorySerializerAdmin(ModelSerializer):
    created = TimeSince(read_only=True)
    service_specialist_detail = SerializerMethodField(
        "get_specialist_name", read_only=True
    )
    icon_url = SerializerMethodField("get_icon", read_only=True)
    icon = ImageField(write_only=True, required=False, allow_empty_file=True)

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
    subcategory_name = SerializerMethodField("get_subcategory_name")
    icon_url = SerializerMethodField("get_icon", read_only=True)
    icon = ImageField(write_only=True, required=False, allow_empty_file=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "price",
            "active",
            "created",
            "description",
            "subcategory",
            "subcategory_name",
            "icon",
            "icon_url",
        )
        read_only_fields = ("created", "active", "subcategory_name")

    def get_icon(self, obj):
        return obj.icon.url

    def get_subcategory_name(self, obj):
        return obj.subcategory.name


class BlogPostAdministrator(ModelSerializer):

    created = TimeSince(read_only=True)
    date_slug = SerializerMethodField(method_name="get_date_slug", read_only=True)
    photo_url = SerializerMethodField(method_name="get_blog_photo", read_only=True)
    photo = ImageField(write_only=True, allow_empty_file=True, required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "category",
            "title",
            "slug",
            "photo",
            "photo_url",
            "body",
            "created",
            "date_slug",
        )

    def get_date_slug(self, obj):
        created_date = obj.created
        return {
            "year": str(created_date.year),
            "month": str(created_date.month),
            "day": str(created_date.day),
        }

    def get_blog_photo(self, obj):
        return obj.photo.url


class CommentSerializerAdmin(ModelSerializer):
    created = TimeSince(read_only=True)
    created_iso = SerializerMethodField("get_date")

    class Meta:
        model = Comment
        fields = (
            "id",
            "parent",
            "post",
            "user",
            "name",
            "email",
            "replies",
            "comment",
            "active",
            "created",
            "created_iso",
        )
        read_only_fields = ("parent", "replies", "created_iso")

    def validate(self, attrs):
        offline_details = attrs.get("name", None) and attrs.get("email", None)
        if not attrs.get("user", None) and not offline_details:
            raise ValidationError(
                "To create a comment you need to be logged in or provide your name and email."
            )
        else:
            return super().validate(attrs)

    def get_date(self, obj):
        return obj.created.strftime("%d, %b %Y  %A, %H")


class CouponSerializerAdministrator(ModelSerializer):

    valid_from_date = SerializerMethodField("get_valid_from", read_only=True)
    valid_to_date = SerializerMethodField("get_valid_to", read_only=True)
    valid_from = DateField(input_formats=(["%d-%m-%Y"]), write_only=True)
    valid_to = DateField(input_formats=(["%d-%m-%Y"]), write_only=True)

    class Meta:
        model = CouponCode
        fields = (
            "id",
            "code",
            "discount",
            "valid_from",
            "valid_from_date",
            "valid_to",
            "valid_to_date",
            "active",
            "category",
            "users",
        )
        extra_kwargs = {
            "valid_from": {"write_only": True},
            "valid_to": {"write_only": True},
        }

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

    def validate(self, attrs):
        # Convert naive Datetime to utc aware
        valid_from_naive = attrs["valid_from"]
        valid_to_naive = attrs["valid_to"]
        valid_from_aware = datetime(
            year=valid_from_naive.year,
            month=valid_from_naive.month,
            day=valid_from_naive.day,
            tzinfo=pytz.UTC,
        )
        valid_to_aware = datetime(
            year=valid_to_naive.year,
            month=valid_to_naive.month,
            day=valid_to_naive.day,
            tzinfo=pytz.UTC,
        )
        if valid_from_aware >= valid_to_aware:
            raise ValidationError(
                "Valid_from date cannot be greater then or equal to Valid_to date"
            )
        elif valid_to_aware < datetime.now().astimezone(pytz.UTC):
            raise ValidationError("Valid_to dates needs to be a future date")
        else:
            attrs["valid_from"] = valid_from_aware
            attrs["valid_to"] = valid_to_aware
            return super().validate(attrs)
