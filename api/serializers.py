from django.db.models import fields
from django.utils.timesince import timesince
from rest_framework.serializers import (Field, ModelSerializer,
                                        SerializerMethodField,
                                        StringRelatedField)

from account.models import CustomUser

from .models import (CategoryReview, Contact, CouponCode, EmployeeCategory,
                     PartnerRequest, Service, ServiceSubcategory)


class EmployeeCategorySerializer(ModelSerializer):
    icon = SerializerMethodField(method_name="get_icon")

    class Meta:
        model = EmployeeCategory
        fields = ["id", "name", "slug", "icon"]

    def get_icon(self, obj):
        return obj.icon.url


class ServiceSerializer(ModelSerializer):
    icon = SerializerMethodField(method_name="get_service_image")
    placeholder = SerializerMethodField(method_name="get_service_placeholder")

    class Meta:
        model = Service
        fields = "__all__"

    def get_service_image(self, obj):
        return obj.icon.url

    def get_service_placeholder(self, obj):
        return obj.placeholder.url


class SubcategorySerializer(ModelSerializer):
    service_specialist = StringRelatedField(read_only=True)
    icon = SerializerMethodField("get_subcategory_image")
    placeholder = SerializerMethodField("get_subcategory_placeholder")

    class Meta:
        model = ServiceSubcategory
        fields = "__all__"

    def get_subcategory_image(self, obj):
        return obj.icon.url

    def get_subcategory_placeholder(self, obj):
        return obj.placeholder.url


class CouponCodeSerializers(ModelSerializer):
    category = StringRelatedField(many=True)

    class Meta:
        model = CouponCode
        fields = ["id", "code", "discount", "category"]


class TimeSince(Field):
    def to_representation(self, value):
        return timesince(value) + " ago"


class ReviewUser(ModelSerializer):
    photo = SerializerMethodField("get_profile_pic")

    class Meta:
        model = CustomUser
        fields = ["number", "username", "email", "photo"]

    def get_profile_pic(self, obj):
        return obj.photo.url


# class CategoryReviewSerializer(ModelSerializer):
#     user = ReviewUser(many=False, read_only=True)
#     created = TimeSince(read_only=True)

#     class Meta:
#         model = CategoryReview
#         fields = ['id' ,'user', 'star', 'replies', 'review', 'parent', 'created']


class CategoryReviewSerializer(ModelSerializer):
    user = ReviewUser(many=False, read_only=True)
    created = TimeSince(read_only=True)

    class Meta:
        model = CategoryReview
        fields = ["id", "user", "star", "replies", "review", "parent", "created"]


class AllSubcategoryServiceSerializer(ModelSerializer):
    services = ServiceSerializer(many=True)

    class Meta:
        model = ServiceSubcategory
        fields = ["id", "name", "slug", "services"]


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ("first_name", "last_name", "email", "message")


class PartnerRequestSerializer(ModelSerializer):
    class Meta:
        model = PartnerRequest
        fields = ("name", "number", "email", "detail")
