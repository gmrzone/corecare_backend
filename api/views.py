from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_406_NOT_ACCEPTABLE)

from account.models import CustomUser
from account.serializers import UserSerializer

from .models import (CategoryReview, CouponCode, EmployeeCategory, Service,
                     ServiceSubcategory)
from .serializers import (AllSubcategoryServiceSerializer,
                          CategoryReviewSerializer, ContactSerializer,
                          CouponCodeSerializers, EmployeeCategorySerializer,
                          PartnerRequestSerializer, ServiceSerializer,
                          SubcategorySerializer)
from .tasks import send_contact_or_partners_mail


@api_view(["GET"])
def EmployeeCategoryList(request):
    employee_category = cache.get("employee_category")
    if employee_category:
        return Response(employee_category)
    else:
        categories = EmployeeCategory.objects.all()
        serializer = EmployeeCategorySerializer(categories, many=True)
        cache.set("employee_category", serializer.data)
        return Response(serializer.data)


# Working Class Views But images url as relative


class GetServiceList(ListAPIView):
    serializer_class = ServiceSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        query = cache.get("service_list")
        if not query:
            query = Service.objects.all()
            cache.set("service_list", query)
        return query


class EmployeeCategoryListView(ListAPIView):
    serializer_class = EmployeeCategorySerializer
    http_method_names = ["get"]

    def get_queryset(self):
        query = cache.get("employee_category")
        if not query:
            query = EmployeeCategory.objects.all()
            cache.set("employee_category", query)
        return query


class GetSubcategoryForSingleCategory(ListAPIView):
    serializer_class = SubcategorySerializer
    http_method_names = ["get"]

    def dispatch(self, request, id, slug, *args, **kwargs):
        self.id = id
        self.slug = slug
        return super().dispatch(request, id, slug, *args, **kwargs)

    def get_queryset(self):
        query = cache.get(f"{self.slug}_subcategory_{self.id}")
        if not query:
            query = ServiceSubcategory.objects.filter(
                service_specialist__id=self.id, service_specialist__slug=self.slug
            ).select_related("service_specialist")
            cache.set(f"{self.slug}_subcategory_{self.id}", query)
        return query


class GetSubcategoryView(ListAPIView):
    serializer_class = SubcategorySerializer
    http_method_names = ["get"]

    def get_queryset(self):
        query = cache.get("subcategory_list")
        if not query:
            query = ServiceSubcategory.objects.all().select_related(
                "service_specialist"
            )
            cache.set("subcategory_list", query)
        return query


class GetEmployeesList(ListAPIView):
    serializer_class = UserSerializer
    http_method_names = ["get"]

    def dispatch(self, request, slug, *args, **kwargs):
        self.slug = slug
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = cache.get(f"{self.slug}_employees")
        if not query:
            query = CustomUser.objects.filter(employee_category__slug=self.slug)
            cache.set(f"{self.slug}_employees", query)
        return query


class GetReviewsList(ListAPIView):
    serializer_class = CategoryReviewSerializer
    http_method_names = ["get"]

    def dispatch(self, request, slug, *args, **kwargs):
        self.slug = slug
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # cache.delete(f"{self.slug}_reviews")
        # query = cache.get(f"{self.slug}_reviews")
        # if not query:
        #     query = CategoryReview.objects.filter(category__slug=self.slug).select_related('user').prefetch_related('replies')
        #     cache.set(f"{self.slug}_reviews", query)
        query = (
            CategoryReview.objects.filter(category__slug=self.slug, parent=None)
            .select_related("user")
            .prefetch_related("replies")
        )
        return query


class GetReplyForReview(ListAPIView):
    serializer_class = CategoryReviewSerializer
    http_method_names = ["get"]

    def dispatch(self, request, parent_id, *args, **kwargs):
        self.parent_id = parent_id
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = (
            CategoryReview.objects.filter(parent__id=self.parent_id)
            .select_related("user")
            .prefetch_related("replies")
        )
        return query


class GetFullServiceList(ListAPIView):
    serializer_class = AllSubcategoryServiceSerializer
    http_method_names = ["get"]

    def dispatch(self, request, slug, *args, **kwargs):
        self.slug = slug
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = cache.get(f"{self.slug}_services")
        if not query:
            query = ServiceSubcategory.objects.filter(
                service_specialist__slug=self.slug
            ).prefetch_related("services")
            cache.set(f"{self.slug}_services", query)
        return query


class SearchServices(ListAPIView):
    serializer_class = SubcategorySerializer
    http_method_names = ["get"]

    def dispatch(self, request, query, city, *args, **kwargs):
        self.query = query
        self.city = city
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        service_sub = ServiceSubcategory.objects.filter(
            name__icontains=self.query
        ).select_related("service_specialist")
        return service_sub


class GetHiringEmployeeCategory(ListAPIView):
    serializer_class = EmployeeCategorySerializer
    http_method_names = ["get"]

    def get_queryset(self):
        query = cache.get("currently_hiring")
        if not query:
            query = EmployeeCategory.objects.filter(hiring=True)
            cache.set("currently_hiring", query)
        return query


class GetCouponsView(ListAPIView):
    http_method_names = ["get"]
    serializer_class = CouponCodeSerializers

    def get_queryset(self):
        queryset = cache.get("coupon_code")
        if not queryset:
            queryset = CouponCode.objects.all().prefetch_related("category")
            cache.set("coupon_code", queryset)
        return queryset


@api_view(["GET"])
def get_subcategory_for_single_category(request, id, slug):
    serialized_data = cache.get(f"{slug}_subcategory_{id}")
    if serialized_data:
        return Response(serialized_data)
    else:
        subcategory = ServiceSubcategory.objects.filter(
            service_specialist__id=id, service_specialist__slug=slug
        ).select_related("service_specialist")
        serializer = SubcategorySerializer(subcategory, many=True)
        cache.set(f"{slug}_subcategory_{id}", serializer.data)
        return Response(serializer.data, status=200)


@api_view(["GET"])
def GetSubcategory(request):
    subcategory = ServiceSubcategory.objects.all().select_related("service_specialist")
    Serializer = SubcategorySerializer(subcategory, many=True)
    return Response(Serializer.data)


@api_view(["GET"])
def GetServices(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getEmployees(request, slug):
    # employees = EmployeeCategory.objects.get(slug=slug).users.all()
    employees = CustomUser.objects.filter(employee_category__slug=slug)
    ser = UserSerializer(employees, many=True)
    return Response(ser.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createReview(request, slug):
    category = EmployeeCategory.objects.get(slug=slug)
    parent_id = request.data.get("parent", False)
    cache.delete(f"{slug}_reviews")
    try:
        parent = CategoryReview.objects.get(id=parent_id)
    except CategoryReview.DoesNotExist:
        review = CategoryReview(
            star=request.data["star"], review=request.data["review"]
        )
    else:
        review = CategoryReview(
            star=request.data["star"], review=request.data["review"], parent=parent
        )
    review.user = request.user
    review.category = category
    # cache.delete(f"{slug}_reviews")
    review.save()
    ser = CategoryReviewSerializer(review)
    return Response(ser.data)


class CreateReview(CreateAPIView):
    http_method_names = ["post"]
    serializer_class = CategoryReviewSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        user = request.user
        category_slug = kwargs["slug"]
        category = get_object_or_404(EmployeeCategory, slug=category_slug)
        if serializer.is_valid():
            serializer.save(user=user, category=category)
            data = {
                "status": "ok",
                "message": "Review added sucessfuly",
                "data": serializer.data,
            }
            status = HTTP_201_CREATED
        else:
            data = {"status": "error", "message": serializer.errors}
            status = HTTP_406_NOT_ACCEPTABLE
        return Response(data=data, status=status)


class UpdateReview(UpdateAPIView):
    serializer_class = CategoryReviewSerializer
    http_method_names = ["patch"]
    lookup_fields = ("category__slug", "id")

    def get_queryset(self):
        queryset = CategoryReview.objects.all()
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.serializer_class(
            instance=instance, data=request.data, partial=partial
        )
        if serializer.is_valid():
            self.perform_update(serializer)
            data = {
                "status": "ok",
                "message": "Review updated sucessfuly",
            }
            status = HTTP_200_OK
        else:
            data = {"status": "error", "message": serializer.errors}
            status = HTTP_406_NOT_ACCEPTABLE
        return Response(data=data, status=status)

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


# class UpdateReview(UpdateAPIView):
#     serializer_class = CategoryReviewSerializer
#     http_method_names = ['patch']
#     lookup_field =

# Class Slow View

# class CreateReview(CreateAPIView):
#     serializer_class = CategoryReviewSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['post']

#     def dispatch(self, request, slug,  *args, **kwargs):
#         self.slug = slug
#         return super().dispatch(request, *args, **kwargs)

#     def create(self, request, *args, **kwargs):
#         category = EmployeeCategory.objects.get(slug=self.slug)
#         parent_id = request.data.get('parent', False)
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             parent_review = None if not parent_id else CategoryReview.objects.get(pk=parent_id)
#             instance = serializer.save(category=category, user=request.user, parent=parent_review)
#             instance.save()
#             if parent_review:
#                 reviews = CategoryReview.objects.filter(category=category).select_related('user', 'parent')
#                 data = CategoryReviewSerializer(reviews, many=True).data
#             else:
#                 data = serializer.data

#             return Response(data)
#         else:
#             return Response({'error': True})


@api_view(["GET"])
def get_full_service(request, slug):
    all_service = ServiceSubcategory.objects.filter(
        service_specialist__slug=slug
    ).prefetch_related("services")
    service_serializer = AllSubcategoryServiceSerializer(all_service, many=True)
    return Response(service_serializer.data)


@api_view(["GET"])
def search_service(request, query, city):
    if query:
        service_sub = ServiceSubcategory.objects.filter(
            name__icontains=query
        ).select_related("service_specialist")
        data = SubcategorySerializer(service_sub, many=True).data
    else:
        data = []
    return Response(data)


@api_view(["GET"])
def getHiringEmployeeCategories(request):
    category = EmployeeCategory.objects.filter(hiring=True)
    ser = EmployeeCategorySerializer(category, many=True)
    return Response(ser.data)


class SendContactAndPartnerMixin:
    def post(self, request, *args, **kwargs):
        data = request.data
        instance = self.serializer_class(data=data)
        if instance.is_valid():
            if self.type == "contact":
                success_msg = "Thank you for contacting us. we Will get back to you as soon as possible"
            elif self.type == "partner":
                success_msg = "Thank you for showing Interest in CoreCare Partners. we Will get back to you as soon as possible"
            try:
                send_contact_or_partners_mail.delay(
                    self.type,
                    data,
                    "saiyedafzal0@gmail.com",
                    ["saiyedafzalgz@gmail.com"],
                )
                # send_mail(mail_subject, mail_message,'saiyedafzal0@gmail.com',['saiyedafzalgz@gmail.com'])
            except Exception as e:
                return Response(
                    {
                        "status": "error",
                        "message": "There was an error on our end please try again later.",
                    }
                )
            else:
                instance.save()
                return Response({"status": "ok", "message": success_msg})
        else:
            return Response(
                {
                    "status": "error",
                    "message": "Please Make sure that your imformation is accurate or try again later",
                }
            )


class CreatePartnerRequest(SendContactAndPartnerMixin, CreateAPIView):
    serializer_class = PartnerRequestSerializer
    type = "partner"


class ContactUs(SendContactAndPartnerMixin, CreateAPIView):
    serializer_class = ContactSerializer
    type = "contact"
