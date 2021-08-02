from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_406_NOT_ACCEPTABLE)

from account.models import CustomUser
from cart.models import Order

from .serializers import *


class AdminCreateMixin:
    serializer_class = NotImplemented
    serializer_success_msg = NotImplemented
    http_method_names = ["post"]
    success_arg = NotImplemented

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        success_param = request.data.get(self.success_arg, None)
        if serializer.is_valid():
            self.perform_create(serializer)
            success_message = (
                self.serializer_success_msg(success_param)
                if success_param
                else self.serializer_success_msg
            )
            data = {"status": "ok", "message": success_message}
            status = HTTP_201_CREATED
        else:
            print(serializer.errors)
            data = {"status": "error", "message": serializer.errors}
            status = HTTP_406_NOT_ACCEPTABLE
        return Response(data=data, status=status)


class AdminRetriveMixin:

    http_method_names = ["get"]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {
            field: self.kwargs[field]
            for field in self.lookup_fields
            if self.kwargs[field]
        }
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AdminUpdateMixin:
    serializer_class = NotImplemented
    serializer_success_msg = NotImplemented
    http_method_names = ["patch"]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.serializer_class(
            instance=instance, data=request.data, partial=partial
        )
        if serializer.is_valid():
            self.perform_update(serializer)
            data = {"status": "ok", "message": self.serializer_success_msg}
            status = HTTP_200_OK
        else:
            data = {"status": "error", "message": serializer.errors}
            status = HTTP_406_NOT_ACCEPTABLE
        return Response(data=data, status=status)


class AdminDestroyMixin:
    serializer_class = None
    serializer_success_msg = NotImplemented
    http_method_names = ["delete"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"status": "ok", "message": self.serializer_success_msg}
        status = HTTP_200_OK
        return Response(data=data, status=status)


# Queryset mixins


class UserQuerysetMixin:
    serializer_class = UserSerializerAdministrator

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset


class EmployeeQuerysetMixin:
    serializer_class = EmployeeSerializerAdministrator

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_employee=True).select_related(
            "employee_category"
        )
        return queryset


class OrderQuerysetMixin:
    serializer_class = OrderSerializerAdministrator

    def get_queryset(self):
        queryset = (
            Order.objects.all()
            .select_related("category", "user", "coupon")
            .prefetch_related("items", "items__service")
        )
        return queryset


class SubcategoryQuerysetMixin:
    serializer_class = ServiceSubcategorySerializerAdmin

    def get_queryset(self):
        queryset = ServiceSubcategory.objects.all().select_related("service_specialist")
        return queryset


class ServiceQueryMixin:
    serializer_class = ServiceSerializerAdministrator

    def get_queryset(self):
        queryset = Service.objects.all().select_related(
            "subcategory", "subcategory__service_specialist"
        )
        return queryset


class BlogPostQuerysetMixin:
    serializer_class = BlogPostAdministrator

    def get_queryset(self):
        queryset = Post.objects.all().select_related("category", "author")
        return queryset


class BlogPostCommentQuerysetMixin:
    serializer_class = CommentSerializerAdmin

    def get_queryset(self):
        queryset = (
            Comment.objects.all().select_related("user").prefetch_related("replies")
        )
        return queryset


class CouponQuerysetMixin:
    serializer_class = CouponSerializerAdministrator

    def get_queryset(self):
        queryset = CouponCode.objects.all().prefetch_related("category", "users")
        return queryset
