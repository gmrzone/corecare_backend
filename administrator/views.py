from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView


from account.utils import get_token, timedelta_to_second


from .mixins import *
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
    serializer_success_msg = "A new user with number {0} has been created sucessfully".format
    success_arg = "number"


# View to update a user
class UpdateUser(UserQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView):
    lookup_fields = ("pk", "number")
    serializer_success_msg = "Update sucessfully"


# View to delete a user
class DeleteUser(
    UserQuerysetMixin, AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView
):
    lookup_fields = ("pk", "number")
    serializer_class = None
    serializer_success_msg = "User has been deleted sucessfully"


#  Get List of Employees
class GetEmployees(EmployeeQuerysetMixin, ListAPIView):

    http_method_names = ["get"]


# Get a single Employee
class GetEmployee(EmployeeQuerysetMixin, AdminRetriveMixin, RetrieveAPIView):
    lookup_fields = ("pk", "number")


# Create a Employee
class CreateEmployee(AdminCreateMixin, CreateAPIView):
    serializer_class = EmployeeSerializerAdministrator
    serializer_success_msg = "A new employee with number {0} has been created sucessfully".format
    success_arg = "number"


# Update a Employee
class UpdateEmployee(
    EmployeeQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView
):
    lookup_fields = ("pk", "number")
    serializer_success_msg = "Employee Update sucessfully"


# Delete a Employee
class DeleteEmployee(
    EmployeeQuerysetMixin, AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView
):
    lookup_fields = ("pk", "number")
    serializer_class = None
    serializer_success_msg = "Employee has been deleted sucessfully"


class GetOrders(OrderQuerysetMixin, ListAPIView):

    http_method_names = ["get"]


class GetOrder(OrderQuerysetMixin, AdminRetriveMixin, RetrieveAPIView):

    lookup_fields = ("receipt", "pk")


class CreateOrder(AdminCreateMixin, CreateAPIView):
    serializer_class = OrderSerializerAdministrator
    serializer_success_msg = "Order has been created sucessfully"
    success_arg = None


class UpdateOrder(
    OrderQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView
):

    lookup_fields = ("receipt", "pk")
    serializer_success_msg = "Order Updated sucessfully"


class DeleteOrder(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("receipt", "pk")
    serializer_class = None
    serializer_success_msg = "Order has been deleted sucessfully"


class GetSubCategories(SubcategoryQuerysetMixin, ListAPIView):
    http_method_names = ["get"]


class GetSubcategory(SubcategoryQuerysetMixin, AdminRetriveMixin, RetrieveAPIView):

    lookup_fields = ("slug", "pk")


class CreateSubCategory(AdminCreateMixin, CreateAPIView):
    serializer_class = ServiceSubcategorySerializerAdmin
    serializer_success_msg = "Subcategory with name {0} has been created sucessfully".format
    permission_classes = [IsSuperUser]
    success_arg = "name"
    


class UpdateSubcategory(
    SubcategoryQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView
):
    lookup_fields = ("slug", "pk")
    serializer_success_msg = "Subcategory has been updated sucessfully"


class DeleteSubcategory(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("slug", "pk")
    serializer_success_msg = "Subcategory has been deleted sucessfully"
    serializer_class = None


class GetServices(ServiceQueryMixin, ListAPIView):

    http_method_names = ["get"]


class GetService(ServiceQueryMixin, RetrieveAPIView):

    lookup_fields = ("created__year", "created__month", "pk")


class CreateService(AdminCreateMixin, CreateAPIView):
    serializer_class = ServiceSerializerAdministrator
    serializer_success_msg = "Service with name {0} been created sucessfully".format
    success_arg = "name"


class UpdateService(
    ServiceQueryMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView
):

    serializer_success_msg = "Service has been updated sucessfully"
    lookup_fields = ("created__year", "created__month", "pk")


class DeleteService(
    ServiceQueryMixin, AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView
):
    lookup_fields = ("created__year", "created__month", "pk")
    serializer_success_msg = "Service Has been deleted sucessfully"
    serializer_class = None


class GetBlogPosts(BlogPostQuerysetMixin, ListAPIView):
    http_method_names = ["get"]


class GetBlogPost(BlogPostQuerysetMixin, AdminRetriveMixin, RetrieveAPIView):

    lookup_fields = ("created__year", "created__month", "created__day", "slug")


class CreateBlogPost(AdminCreateMixin, CreateAPIView):
    serializer_class = BlogPostAdministrator
    serializer_success_msg = "Post with title {0} has been created sucessfully".format
    success_arg = "title"



class UpdateBlogPost(
    BlogPostQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView
):
    serializer_success_msg = "Blog post has been updated sucessfully"
    lookup_fields = ("created__year", "created__month", "created__day", "slug")


class DeleteBlogPost(AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView):
    lookup_fields = ("created__year", "created__month", "created__day", "slug")
    serializer_success_msg = "Post has been Deleted sucessfully"
    serializer_class = None


class GetBlogPostComments(BlogPostCommentQuerysetMixin, ListAPIView):
    http_method_names = ["get"]


class GetBlogPostComment(
    BlogPostCommentQuerysetMixin, AdminRetriveMixin, RetrieveAPIView
):
    lookup_fields = ("created__year", "created__month", "created__day", "pk")


class CreateBlogPostComment(AdminCreateMixin, CreateAPIView):
    serializer_class = CommentSerializerAdmin
    serializer_success_msg = "Comment has been created sucessfully"
    success_arg = None


class UpdateBlogPostComment(
    BlogPostCommentQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView
):
    serializer_success_msg = "Comment has been updated sucessfully"
    lookup_fields = ("created__year", "created__month", "created__day", "pk")


class DeleteBlogPostComment(
    BlogPostCommentQuerysetMixin, AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView
):
    lookup_fields = ("created__year", "created__month", "created__day", "pk")
    serializer_success_msg = "Comment has been deleted sucessfully"
    serializer_class = None


class GetCoupons(CouponQuerysetMixin, ListAPIView):
    http_method_names = ["get"]


class GetCoupon(CouponQuerysetMixin, AdminRetriveMixin, RetrieveAPIView):
    lookup_fields = ("code", "pk")


class CreateCoupon(AdminCreateMixin, CreateAPIView):
    serializer_class = CouponSerializerAdministrator
    serializer_success_msg = "Coupon code {0} has been created sucessfully".format
    success_arg = 'code'


class UpdateCoupon(
    CouponQuerysetMixin, AdminUpdateMixin, AdminRetriveMixin, UpdateAPIView
):
    lookup_fields = ("code", "pk")
    serializer_success_msg = "Coupon has been updated sucessfully"


class DeleteCouponCode(
    CouponQuerysetMixin, AdminDestroyMixin, AdminRetriveMixin, DestroyAPIView
):
    serializer_success_msg = "Coupon Code has been deleted Sucessfully"
    lookup_fields = ("code", "pk")
    serializer_class = None
