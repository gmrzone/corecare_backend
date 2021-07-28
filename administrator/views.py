from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView, get_object_or_404)
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView

from account.models import CustomUser
from account.utils import get_token, timedelta_to_second
from api.models import CouponCode, Service, ServiceSubcategory
from blog.models import Comment, Post
from cart.models import Order

from .mixins import AdminCreateMixin, AdminRetriveMixin, AdminUpdateMixin, AdminDestroyMixin
from .permissions import IsSuperUser
from .serializers import *

# Create your views here.


class AdminLogin(APIView):

    http_method_names = ["post"]

    def post(self, request):
        number = request.data.get("number")
        password = request.data.get("password")
        response = Response()
        if number and password:
            user = authenticate(request, number=number, password=password)
            if user:
                if user.is_active:
                    if user.is_superuser:
                        tokens = get_token(user)
                        access_expire = timedelta_to_second(
                            settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME")
                        )
                        refresh_expire = timedelta_to_second(
                            settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME")
                        )
                        response.set_cookie(
                            settings.SIMPLE_JWT.get("AUTH_COOKIE"),
                            tokens["access"],
                            expires=access_expire,
                            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE"),
                            httponly=settings.SIMPLE_JWT.get("AUTH_COOKIE_HTTP_ONLY"),
                            path=settings.SIMPLE_JWT.get("AUTH_COOKIE_PATH"),
                            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE"),
                        )
                        response.set_cookie(
                            settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH"),
                            tokens["refresh"],
                            expires=refresh_expire,
                            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE"),
                            httponly=settings.SIMPLE_JWT.get("AUTH_COOKIE_HTTP_ONLY"),
                            path=settings.SIMPLE_JWT.get("AUTH_COOKIE_PATH"),
                            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE"),
                        )
                        data = {"status": "ok", "message": "Sucessfully logged in"}
                        status = HTTP_200_OK
                    else:
                        response.delete_cookie(settings.SIMPLE_JWT.get("AUTH_COOKIE"))
                        response.delete_cookie(
                            settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH")
                        )
                        data = {
                            "status": "error",
                            "message": "Only admin can use to this website",
                        }
                        status = HTTP_400_BAD_REQUEST
                else:
                    data = {
                        "status": "error",
                        "message": "Your account has been disabled for security reasons.",
                    }
                    status = HTTP_400_BAD_REQUEST
            else:
                data = {
                    "status": "error",
                    "message": "Invalid number or password please try again.",
                }
                status = HTTP_404_NOT_FOUND
        else:
            data = {
                "status": "error",
                "message": "Both number and password is required to login",
            }
            status = HTTP_406_NOT_ACCEPTABLE
        response.data = data
        response.status_code = status
        return response


class GetCurrentUser(APIView):
    http_method_names = ["get"]
    permission_classes = [IsSuperUser]

    def get(self, request):
        user = request.user
        serializer = UserSerializerAdministrator(user)
        return Response(serializer.data, status=HTTP_200_OK)


class GetUsers(ListAPIView):
    serializer_class = UserSerializerAdministrator
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()


class GetUser(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = UserSerializerAdministrator
    lookup_fields = ("pk", "number")

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset


class CreateUser(AdminCreateMixin, CreateAPIView):
    serializer_class = UserSerializerAdministrator
    serializer_success_msg = "A new user has been created sucessfully"

class UpdateUser(AdminUpdateMixin , AdminRetriveMixin, UpdateAPIView):

    serializer_class = UserSerializerAdministrator
    lookup_fields = ("pk", "number")
    serializer_success_msg = "Update sucessfully"


    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset

class DeleteUser(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("pk", "number")

    def get_queryset(self):
        queryset = queryset = CustomUser.objects.all()
        return queryset


class GetEmployees(ListAPIView):
    serializer_class = EmployeeSerializerAdministrator
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_employee=True).select_related(
            "employee_category"
        )
        return queryset


class GetEmployee(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = EmployeeSerializerAdministrator
    lookup_fields = ("pk", "number")

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_employee=True).select_related(
            "employee_category"
        )
        return queryset


class CreateEmployee(AdminCreateMixin, CreateAPIView):
    serializer_class = EmployeeSerializerAdministrator
    serializer_success_msg = "A new employee has been created sucessfully"


class UpdateEmployee(AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    serializer_class = EmployeeSerializerAdministrator
    serializer_success_msg = "Employee Update sucessfully"
    lookup_fields = ('pk', 'number')

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_employee=True).select_related(
            "employee_category"
        )
        return queryset



class GetOrders(ListAPIView):
    serializer_class = OrderSerializerAdministrator
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = (
            Order.objects.all()
            .select_related("category", "user", "coupon")
            .prefetch_related("items", "items__service", "coupon__category")
        )
        return queryset


class GetOrder(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = OrderSerializerAdministrator
    lookup_fields = ("receipt", "pk")

    def get_queryset(self):
        queryset = (
            Order.objects.all()
            .select_related("category", "user", "coupon")
            .prefetch_related("items", "items__service", "coupon__category")
        )
        return queryset


class CreateOrder(AdminCreateMixin, CreateAPIView):
    serializer_class = OrderSerializerAdministrator
    serializer_success_msg = "Order has been created sucessfully"
    # permission_classes = [IsSuperUser]

class UpdateOrder(AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    serializer_class = OrderSerializerAdministrator
    lookup_fields = ("receipt", "pk")
    serializer_success_msg = "Order Updated sucessfully"

    def get_queryset(self):
        queryset = (
            Order.objects.all()
            .select_related("category", "user", "coupon")
            .prefetch_related("items", "items__service", "coupon__category")
        )
        return queryset


class GetSubCategories(ListAPIView):
    serializer_class = ServiceSubcategorySerializerAdmin
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = ServiceSubcategory.objects.all().select_related("service_specialist")
        return queryset


class GetSubcategory(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = ServiceSubcategorySerializerAdmin
    lookup_fields = ("slug", "pk")

    def get_queryset(self):
        queryset = ServiceSubcategory.objects.all().select_related("service_specialist")
        return queryset


class CreateSubCategory(AdminCreateMixin, CreateAPIView):
    serializer_class = ServiceSubcategorySerializerAdmin
    serializer_success_msg = "Subcategory has been created sucessfully"
    permission_classes = [IsSuperUser]


class GetServices(ListAPIView):
    serializer_class = ServiceSerializerAdministrator
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = Service.objects.all().select_related(
            "subcategory", "subcategory__service_specialist"
        )
        return queryset


class GetService(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = ServiceSerializerAdministrator
    lookup_fields = ("created__year", "created__month", "pk")

    def get_queryset(self):
        queryset = Service.objects.all().select_related(
            "subcategory", "subcategory__service_specialist"
        )
        return queryset


class CreateService(AdminCreateMixin, CreateAPIView):
    serializer_class = ServiceSerializerAdministrator
    serializer_success_msg = "Service has been created sucessfully"


class GetBlogPosts(ListAPIView):
    serializer_class = BlogPostAdministrator
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = Post.objects.all().select_related("category", "author")
        return queryset


class GetBlogPost(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = BlogPostAdministrator
    lookup_fields = ("created__year", "created__month", "created__day", "slug")

    def get_queryset(self):
        queryset = Post.objects.all().select_related("category", "author")
        return queryset


class CreateBlogPost(AdminCreateMixin, CreateAPIView):
    serializer_class = BlogPostAdministrator
    serializer_success_msg = "Post has been created sucessfully"


class GetBlogPostComments(ListAPIView):
    serializer_class = CommentSerializerAdmin
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = (
            Comment.objects.all().select_related("user").prefetch_related("replies")
        )
        return queryset


class GetBlogPostComment(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = CommentSerializerAdmin
    lookup_fields = ("created__year", "created__month", "created__day", "pk")

    def get_queryset(self):
        queryset = (
            Comment.objects.all().select_related("user").prefetch_related("replies")
        )
        return queryset


class CreateBlogPostComment(AdminCreateMixin, CreateAPIView):
    serializer_class = CommentSerializerAdmin
    serializer_success_msg = "Comment has been created sucessfully"


class GetCoupons(ListAPIView):
    serializer_class = CouponSerializerAdministrator
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = CouponCode.objects.all().prefetch_related("category", "users")
        return queryset


class GetCoupon(AdminRetriveMixin, RetrieveAPIView):
    serializer_class = CouponSerializerAdministrator
    lookup_fields = ("code", "pk")

    def get_queryset(self):
        queryset = CouponCode.objects.all().prefetch_related("category", "users")
        return queryset


class CreateCoupon(AdminCreateMixin, CreateAPIView):
    serializer_class = CouponSerializerAdministrator
    serializer_success_msg = "Coupon has been created sucessfully"
