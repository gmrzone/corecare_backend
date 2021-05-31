
from django.db.models import fields
from .models import EmployeeCategory, CouponCode, ServiceSubcategory, Service, CategoryReview, Contact, PartnerRequest
from rest_framework.serializers import ModelSerializer, StringRelatedField, Field, SerializerMethodField
from django.utils.timesince import timesince
from account.models import CustomUser


class EmployeeCategorySerializer(ModelSerializer):
    class Meta:
        model = EmployeeCategory
        fields = ['id', 'name', 'slug', 'icon']

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields= '__all__'

class SubcategorySerializer(ModelSerializer):
    service_specialist = EmployeeCategorySerializer()
    icon = SerializerMethodField(method_name="get_icon")
    class Meta:
        model = ServiceSubcategory
        fields = '__all__'

    def get_icon(self, obj):
        return obj.icon.url

class CouponCodeSerializers(ModelSerializer):
    category = StringRelatedField(many=True)
    class Meta:
        model = CouponCode
        fields = ['id' ,'code', 'discount', 'category']

class TimeSince(Field):
    def to_representation(self, value):
        return timesince(value) + " ago"

class ReviewUser(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['number', 'username', 'email', 'photo']

class CategoryReviewSerializer(ModelSerializer):
    user = ReviewUser(many=False, read_only=True)
    created = TimeSince(read_only=True)

    class Meta:
        model = CategoryReview
        fields = ['id' ,'user', 'star', 'replies', 'review', 'parent', 'created']


class AllSubcategoryServiceSerializer(ModelSerializer):
    services = ServiceSerializer(many=True)
    class Meta:
        model = ServiceSubcategory
        fields = ['id' ,'name', 'slug', 'services']

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'message')

class PartnerRequestSerializer(ModelSerializer):
    class Meta:
        model = PartnerRequest
        fields = ('name', 'number', 'email', 'detail')