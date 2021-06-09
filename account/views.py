# RestFramework
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from .tasks import new_signup
from rest_framework import status
from rest_framework.schemas import ManualSchema
import coreapi
from rest_framework.schemas.coreapi import coreschema
# Serializers
from .serializers import UserSerializer

# Project Modules
from .utils import generate_key_for_otp, generate_key_for_otp, get_token, timedelta_to_second

# Other Imports
import base64
import pyotp
# Models
from .models import CustomUser

# Django Imports
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf

# Create your views here.
@api_view(['GET'])
def get_csrf(request):
    token = csrf.get_token(request)
    response = Response()
    response['X-CSRFToken'] = token
    response.data = {'status': "success"}
    return response


class LoginView(APIView):

    schema = ManualSchema(fields=[coreapi.Field('number', required=True, location='form', schema=coreschema.String()), coreapi.Field('password', required=True, location="form", schema=coreschema.String())])
    def post(self, request):
        data = request.data
        response = Response()
        number = data.get('number')
        password = data.get('password')
        user = authenticate(number=number, password=password)
        if user is not None:
            if user.is_active:
                data = get_token(user)
                access_expire = timedelta_to_second(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
                refresh_expire = timedelta_to_second(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data['access'],
                    expires=access_expire,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=data['refresh'],
                    expires=refresh_expire,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                # csrf.get_token(request)
                response.data = {"status": "success", 'msg': "Login Successfull.", "data":data, "expire": refresh_expire}
                return response
            else:
                return Response(data={"status": "error", 'msg': "Your account has been disabled for security reasons."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data={"status": "error", 'msg': "Invalid number or password"}, status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):

    schema = ManualSchema(fields=[coreapi.Field('X-CSRFToken', required=True, location='header', schema=coreschema.String())])
    def post(self, request):
        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        # response.delete_cookie('get_user')
        response.data = {'status': "ok", "msg": "Successfully Logout"}
        return response


class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated]  
    http_method_names = ['get']
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class SignUp(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    schema = ManualSchema(fields=[coreapi.Field('number', required=True, location='form', schema=coreschema.String()), coreapi.Field('X-CSRFToken', required=True, location='header', schema=coreschema.String())])
    def create(self, request, *args, **kwargs):
        number = request.data.get('number')
        try:
            user = CustomUser.objects.get(number=number)
            if not user.verified:
                user.delete()
                raise CustomUser.DoesNotExist()
        except CustomUser.DoesNotExist:
            serializer =self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.save()
            else:
                data = {'status': 'error', 'msg': serializer.error_messages}
        else:
            data = {'status': 'warning', 'msg': 'An Account with number {0} already Exist with us. Please Login or Reset Your Password.'.format(number)}
        return Response(data)       



def update_user(user, first_name, last_name, email, address_1, address_2, city, state, pincode, new_account):
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.address_1 = address_1
    user.address_2 = address_2
    user.city = city
    user.state = state
    user.pincode = pincode
    user.save()
    if new_account:
        new_signup.delay(user.id)

@api_view(['POST'])
def signup_additional(request):
    user = request.user
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    address_1 = request.data.get('address_1')
    address_2 = request.data.get('address_2')
    city = request.data.get('city')
    state = request.data.get('state')
    pincode = request.data.get('pincode')
    number = request.data.get('number')
    password = request.data.get('password')
    email_exist = CustomUser.objects.filter(email=email).exists()
    if isinstance(user, AnonymousUser):
        if first_name and last_name and email and address_1 and address_2 and city and state and pincode and number:
            if email_exist:
                data = {'status': 'error', 'msg': 'We Already have an account associated with email {0}'.format(email)}
            else:
                user = get_object_or_404(CustomUser, number=number)
                if user.check_password(password):
                    update_user(user, first_name, last_name, email, address_1, address_2, city, state, pincode, new_account=True)
                    data = {'status': 'ok', 'msg': 'Profile Sucessfully Updated'}
                else:
                    data = {'status': 'error', 'msg': 'Invalid Number'}
        else:
            data = {'status': 'error', 'msg': 'Please Provide all the required fields'}
    else:
        if email_exist:
            data = {'status': 'error', 'msg': 'We Already have an account associated with email {0}'.format(email)}
        else:
            update_user(user, first_name, last_name, email, address_1, address_2, city, state, pincode, new_account=False)
            data = {'status': 'ok', 'msg': 'Profile Sucessfully Updated'}
    return Response(data)

class UpdateSignupAdditionalData(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch']
    schema = ManualSchema(fields=[coreapi.Field('X-CSRFToken', required=True, location='header', schema=coreschema.String()), coreapi.Field('number', required=True, location='query', schema=coreschema.String()), coreapi.Field('username', required=True, location='form', schema=coreschema.String()), coreapi.Field('first_name', required=True, location='form', schema=coreschema.String()), coreapi.Field('last_name', required=True, location='form', schema=coreschema.String()), coreapi.Field('email', required=True, location='form', schema=coreschema.String()), coreapi.Field('address_1', required=True, location='form', schema=coreschema.String()), coreapi.Field('address_2', required=True, location='form', schema=coreschema.String()), coreapi.Field('city', required=True, location='form', schema=coreschema.String()), coreapi.Field('state', required=True, location='form', schema=coreschema.String()), coreapi.Field('pincode', required=True, location='form', schema=coreschema.String())])

    def update(self, request, number, *args, **kwargs):
        try:
            request_data = {
                "first_name": request.data['first_name'],
                "last_name": request.data['last_name'],
                "email": request.data['email'],
                "address_1": request.data['address_1'],
                "address_2": request.data['address_2'],
                "city": request.data['city'],
                "state": request.data['state'],
                'pincode': request.data['pincode']
                }
        except KeyError:
            data = {'status': 'error', 'msg': 'Please Provide all the required fields'}
        else:
            user = request.user
            # number = request.data.get('number')
            password = request.data.get('password')
            isAnonUser = isinstance(user, AnonymousUser)
            if isAnonUser:
                instance = get_object_or_404(CustomUser, number=number)
                if not instance.check_password(password):
                    return Response({'status': 'error', 'msg': 'Invalid Number'})
            else:
                instance = user
            serializer = UserSerializer(instance=instance, data=request_data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                data = {'status': 'ok', 'msg': 'Profile Sucessfully Updated'}
            else:
                data = {"error": 'ok', "message": serializer.errors}
        return Response(data)



class VerifyOtp(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request):
        number = request.data.get('number')
        entered_otp = request.data.get('entered_otp')
        password = request.data.get('password1')
        if entered_otp and len(entered_otp) == 6:
            secret_key = generate_key_for_otp(number)
            key = base64.b32encode(secret_key.encode())
            otp = pyotp.TOTP(key, interval=300, digits=6)
            if otp.verify(entered_otp):
                user = get_object_or_404(CustomUser, number=number)
                user.set_password(password)
                user.verified = True
                user.save()
                data = {'status': 'ok', 'msg': 'Your Number Has been Verified Sucessfully'}
            else:
                data = {'status': 'error', 'msg': 'Invalid OTP or OTP Expired'}
        else:
            data = {'status': 'error', 'msg': 'Please Enter a valid 6 digit OTP'}
        return Response(data)



@api_view(['POST'])
@permission_classes([AllowAny])
def update_profile_image(request):
    image = request.data.get('image')
    number = request.data.get('number')
    password = request.data.get('password')
    user = get_object_or_404(CustomUser, number=number)
    if user.check_password(password):
        if image:
            user.photo = image
        user.save()
        data = {'status': 'ok', 'message': 'Profile Photo Updated'}
    else:
        data = {'status': 'error', 'message': "Invalid Number"}
    return Response(data)

class UpdateProfileImage(UpdateAPIView):
    serializer_class = UserSerializer
    http_method_names = ['patch']
    permission_classes = [AllowAny]

    def update(self, request, number, *args, **kwargs):
        instance = CustomUser.objects.get(number=number)
        image = request.data.get('image')
        print(image)
        password = request.data.get('password')
        if instance.check_password(password):
            serializer = UserSerializer(instance=instance, data={'photo': image}, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                data = {'status': 'ok', 'message': 'Profile Photo Updated'}
            else:
                if image:
                    data = {'status': 'error', 'message': 'Invalid or Unsupported Image File'}
                else:
                    data = {'status': 'ok', 'message': 'No profile photo updated using default Avatar.'}
        else:
            data = {'status': 'error', 'message': "Invalid Number"}
        return Response(data)

        







