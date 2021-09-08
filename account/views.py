# RestFramework
# Other Imports
import base64

import pyotp
from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
# Django Imports
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Models
from .models import CustomUser
# Serializers
from .serializers import UserSerializer
from .tasks import new_signup
# Project Modules
from .utils import generate_key_for_otp, get_token, timedelta_to_second


# Create your views here.
@api_view(["GET"])
def get_csrf(request):
    token = csrf.get_token(request)
    response = Response()
    response["X-CSRFToken"] = token
    response.data = {"status": "success"}
    return response


class LoginView(APIView):
    def post(self, request):
        data = request.data
        response = Response()
        number = data.get("number")
        password = data.get("password")
        user = authenticate(number=number, password=password)
        if user is not None:
            if user.is_active:
                data = get_token(user)
                access_expire = timedelta_to_second(
                    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
                )
                refresh_expire = timedelta_to_second(
                    settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=access_expire,
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                    value=data["refresh"],
                    expires=refresh_expire,
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                # csrf.get_token(request)
                response.data = {
                    "status": "success",
                    "msg": "Login Successfull.",
                    "data": data,
                    "expire": refresh_expire,
                }
                return response
            else:
                return Response(
                    data={
                        "status": "error",
                        "msg": "Your account has been disabled for security reasons.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                data={"status": "error", "msg": "Invalid number or password"},
                status=status.HTTP_404_NOT_FOUND,
            )


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        # response.delete_cookie('get_user')
        response.data = {"status": "ok", "msg": "Successfully Logout"}
        return response


class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUp(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        number = request.data.get("number")
        try:
            user = CustomUser.objects.get(number=number)
            if not user.verified:
                user.delete()
                raise CustomUser.DoesNotExist()
        except CustomUser.DoesNotExist:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.save()
                hstatus = status.HTTP_200_OK
            else:
                data = {"status": "error", "msg": serializer.error_messages}
                hstatus = status.HTTP_400_BAD_REQUEST
        else:
            data = {
                "status": "error",
                "msg": "An Account with number {0} already Exist with us. Please Login or Reset Your Password.".format(
                    number
                ),
            }
            hstatus = status.HTTP_406_NOT_ACCEPTABLE
        return Response(data, status=hstatus)


class UpdateSignupAdditionalData(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ["patch"]

    def update(self, request, number, *args, **kwargs):
        password = request.data.get("password")
        if request.user.is_authenticated:
            instance = request.user
            new_user = False
        else:
            instance = get_object_or_404(CustomUser, number=number)
            new_user = True
            if not instance.check_password(password):
                return Response(
                    {"status": "error", "msg": "Invalid Number or Password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        serializer = self.serializer_class(
            instance=instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            self.perform_update(serializer)
            if new_user:
                new_signup.delay(instance.id)
            data = {"status": "ok", "msg": "Profile Sucessfully Updated"}
            hstatus = status.HTTP_200_OK
        else:
            data = {"error": "ok", "msg": serializer.errors}
            hstatus = status.HTTP_406_NOT_ACCEPTABLE
        return Response(data, status=hstatus)


class VerifyOtp(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["post"]
    number = None

    def dispatch(self, request, number, *args, **kwargs):
        self.number = number
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        entered_otp = request.data.get("entered_otp")
        password = request.data.get("password1")
        conf_password = request.data.get("password2")
        if password == conf_password:
            if entered_otp and len(entered_otp) == 6:
                secret_key = generate_key_for_otp(self.number)
                key = base64.b32encode(secret_key.encode())
                otp = pyotp.TOTP(key, interval=300, digits=6)
                if otp.verify(entered_otp):
                    user = get_object_or_404(CustomUser, number=self.number)
                    user.set_password(password)
                    user.verified = True
                    user.save()
                    data = {
                        "status": "ok",
                        "msg": "Your Number Has been Verified Sucessfully",
                    }
                    hstatus = status.HTTP_200_OK
                else:
                    data = {"status": "error", "msg": "Invalid OTP or OTP Expired"}
                    hstatus = status.HTTP_408_REQUEST_TIMEOUT
            else:
                data = {"status": "error", "msg": "Please Enter a valid 6 digit OTP"}
                hstatus = status.HTTP_400_BAD_REQUEST
        else:
            data = {
                "status": "error",
                "msg": "Both password dont match. Please try again.",
            }
            hstatus = status.HTTP_400_BAD_REQUEST
        return Response(data, status=hstatus)


class UpdateProfileImage(UpdateAPIView):
    serializer_class = UserSerializer
    http_method_names = ["patch"]
    permission_classes = [AllowAny]

    def update(self, request, number, *args, **kwargs):
        instance = CustomUser.objects.get(number=number)
        image = request.data.get("image")
        password = request.data.get("password")
        if instance.check_password(password):
            serializer = UserSerializer(
                instance=instance, data={"photo": image}, partial=True
            )
            if serializer.is_valid():
                self.perform_update(serializer)
                data = {"status": "ok", "message": "Profile Photo Updated"}
                hstatus = status.HTTP_200_OK
            else:
                if image:
                    data = {
                        "status": "error",
                        "message": "Invalid or Unsupported Image File",
                    }
                    hstatus = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    data = {
                        "status": "ok",
                        "message": "No profile photo updated using default Avatar.",
                    }
                    hstatus = status.HTTP_200_OK
        else:
            data = {"status": "error", "message": "Invalid Number"}
            hstatus = status.HTTP_401_UNAUTHORIZED
        return Response(data, status=hstatus)
