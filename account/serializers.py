from api.models import EmployeeCategory
from .models import CustomUser
from rest_framework.serializers import ModelSerializer, RelatedField

# Project Modules
from .utils import generate_key_for_otp, generate_key_for_otp
import base64
import pyotp


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'number', 'username', 'email', 'first_name', 'photo', 'last_name', 'verified', 'address_1', 'address_2', 'city', 'state', 'pincode', 'is_active', 'is_employee', 'is_verified_employee']
        extra_kwargs = {'number': {'error_messages': {'required': "Number cannot be Blank please provide a valid number.", 'unique': "A User With Number Already Exist"}}}

    def create(self, validated_data):
        number = validated_data.get('number')
        self.Meta.model.objects.create_user(number=number, password=f"{number}corecare")
        secret_key = generate_key_for_otp(number)
        key = base64.b32encode(secret_key.encode())
        otp = pyotp.TOTP(key, interval=300, digits=6)
        return {'status': 'ok', 'msg': "A 6 Digit OTP Has Been Send to Your Mobile Number {0}".format(number), 'otp': otp.now()}


