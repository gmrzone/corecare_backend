
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from .serializers import *
from account.models import CustomUser
from cart.models import Order
from api.models import ServiceSubcategory, Service, CouponCode
from .permissions import IsSuperUser
from api.serializers import SubcategorySerializer
from blog.models import Post, Comment
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND


# Create your views here.



class GetUsers(ListAPIView):
    serializer_class = UserSerializerAdministrator
    http_method_names = ['get']
    permission_classes = [IsSuperUser]
    queryset = CustomUser.objects.all()


class CreateUser(CreateAPIView):
    serializer_class = UserSerializerAdministrator
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, )
        if serializer.is_valid():
            self.perform_create(serializer)
            data = {'status': "ok", "message": "A New user has been added sucessfully."}
            status = HTTP_200_OK
        else:
            data = {'status': "error", "message": "Please make sure all the required fields have been filled."}
            status = HTTP_404_NOT_FOUND

        return Response(data=data, status=status)



class GetEmployees(ListAPIView):
    serializer_class = UserSerializerAdministrator
    permission_classes = [IsSuperUser]
    http_method_names = ['get']
    

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_employee=True)
        return queryset

class GetOrders(ListAPIView):
    serializer_class = OrderSerializerAdministrator
    permission_classes = [IsSuperUser]
    http_method_names = ['get']
    

    def get_queryset(self):
        queryset = Order.objects.all().select_related('category', 'user', 'coupon').prefetch_related('items', 'items__service', 'coupon__category')
        return queryset


class GetCategories(ListAPIView):
    serializer_class = SubcategorySerializer
    permission_classes = [IsSuperUser]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = ServiceSubcategory.objects.all().select_related('service_specialist')
        return queryset


class GetServices(ListAPIView):
    serializer_class = ServiceSerializerAdministrator
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Service.objects.all().select_related('subcategory', 'subcategory__service_specialist')
        return queryset
        

class GetBlogPosts(ListAPIView):
    serializer_class = BlogPostAdministrator
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Post.objects.all().select_related('category', 'author')
        return queryset

class GetBlogPostComments(ListAPIView):
    serializer_class = CommentSerializerAdmin
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Comment.objects.all().select_related('user').prefetch_related('replies')
        return queryset

class GetCoupons(ListAPIView):
    serializer_class = CouponSerializerAdministrator
    http_method_names = ['get']

    def get_queryset(self):
        queryset = CouponCode.objects.all().prefetch_related('category', 'users')
        return queryset