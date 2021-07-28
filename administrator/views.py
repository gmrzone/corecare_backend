from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
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

from .mixins import (AdminCreateMixin, AdminDestroyMixin, AdminRetriveMixin,
                     AdminUpdateMixin, UserQuerysetMixin, EmployeeQuerysetMixin)
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

# View to get list of users
class GetUsers(UserQuerysetMixin, ListAPIView):
    http_method_names = ["get"]


# View to get single user
class GetUser(UserQuerysetMixin, AdminRetriveMixin, RetrieveAPIView):
    lookup_fields = ("pk", "number")

# View to create a user
class CreateUser(AdminCreateMixin, CreateAPIView):

    serializer_class = UserSerializerAdministrator
    serializer_success_msg = "A new user has been created sucessfully"

# View to update a user
class UpdateUser(UserQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    lookup_fields = ("pk", "number")
    serializer_success_msg = "Update sucessfully"

    
# View to delete a user
class DeleteUser(UserQuerysetMixin, AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("pk", "number")
    serializer_class = None
    serializer_success_msg = "User has been deleted sucessfully"


#  Get List of Employees
class GetEmployees(EmployeeQuerysetMixin ,ListAPIView):

    http_method_names = ["get"]


# Get a single Employee
class GetEmployee(EmployeeQuerysetMixin, AdminRetriveMixin, RetrieveAPIView):
    lookup_fields = ("pk", "number")

# Create a Employee
class CreateEmployee(AdminCreateMixin, CreateAPIView):
    serializer_class = EmployeeSerializerAdministrator
    serializer_success_msg = "A new employee has been created sucessfully"


# Update a Employee
class UpdateEmployee(EmployeeQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    lookup_fields = ("pk", "number")
    serializer_success_msg = "Employee Update sucessfully"


# Delete a Employee
class DeleteEmployee(EmployeeQuerysetMixin, AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("pk", "number")
    serializer_class = None
    serializer_success_msg = "Employee has been deleted sucessfully"




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


class DeleteOrder(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("receipt", "pk")
    serializer_success_msg = "Order has been deleted sucessfully"

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


class UpdateSubcategory(AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    lookup_fields = ("slug", "pk")
    serializer_class = ServiceSubcategorySerializerAdmin
    serializer_success_msg = "Subcategory has been updated sucessfully"

    def get_queryset(self):
        queryset = ServiceSubcategory.objects.all().select_related("service_specialist")
        return queryset

class DeleteSubcategory(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("slug", "pk")
    serializer_success_msg = "Subcategory has been deleted sucessfully"

    def get_queryset(self):
        queryset = ServiceSubcategory.objects.all().select_related("service_specialist")
        return queryset


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


class UpdateService(AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    serializer_class = ServiceSerializerAdministrator
    serializer_success_msg = "Service has been updated sucessfully"
    lookup_fields = ("created__year", "created__month", "pk")

    def get_queryset(self):
        queryset = Service.objects.all().select_related(
            "subcategory", "subcategory__service_specialist"
        )
        return queryset

class DeleteService(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("created__year", "created__month", "pk")
    serializer_success_msg = "Service Has been deleted sucessfully"

    def get_queryset(self):
        queryset = Service.objects.all().select_related(
            "subcategory", "subcategory__service_specialist"
        )
        return queryset


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


class UpdateBlogPost(AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    serializer_success_msg = "Blog post has been updated sucessfully"
    serializer_class = BlogPostAdministrator
    lookup_fields = ("created__year", "created__month", "created__day", "slug")

    def get_queryset(self):
        queryset = Post.objects.all().select_related("category", "author")
        return queryset

class DeleteBlogPost(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("created__year", "created__month", "created__day", "slug")
    serializer_success_msg = "Post has been Deleted sucessfully"

    def get_queryset(self):
        queryset = Post.objects.all().select_related("category", "author")
        return queryset


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


class UpdateBlogPostComment(AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    serializer_class = CommentSerializerAdmin
    serializer_success_msg = "Comment has been updated sucessfully"
    lookup_fields = ("created__year", "created__month", "created__day", "pk")

    def get_queryset(self):
        queryset = (
            Comment.objects.all().select_related("user").prefetch_related("replies")
        )
        return queryset

class DeleteBlogPostComment(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("created__year", "created__month", "created__day", "pk")
    serializer_success_msg = "Comment has been deleted sucessfully"

    def get_queryset(self):
        queryset = (
            Comment.objects.all().select_related("user").prefetch_related("replies")
        )
        return queryset


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


class UpdateCoupon(AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    serializer_class = CouponSerializerAdministrator
    lookup_fields = ("code", "pk")
    serializer_success_msg = "Coupon has been updated sucessfully"

    def get_queryset(self):
        queryset = CouponCode.objects.all().prefetch_related("category", "users")
        return queryset

class DeleteCouponCode(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    serializer_success_msg = "Coupon Code has been deleted Sucessfully"
    lookup_fields = ("code", "pk")

    def get_queryset(self):
        queryset = CouponCode.objects.all().prefetch_related("category", "users")
        return queryset
