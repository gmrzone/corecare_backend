from .models import CustomUser
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'number', 'username', 'email', 'first_name', 'photo', 'last_name', 'verified', 'address_1', 'address_2', 'city', 'state', 'pincode', 'is_active', 'is_employee', 'is_verified_employee']