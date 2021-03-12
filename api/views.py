
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import CategoryReview, EmployeeCategory, CouponCode, Service, ServiceSubcategory
from .serializers import CouponCodeSerializers, EmployeeCategorySerializer, SubcategorySerializer, ServiceSerializer, CategoryReviewSerializer, AllSubcategoryServiceSerializer
from rest_framework.permissions import IsAuthenticated
from account.serializers import UserSerializer
from itertools import chain
from django.core.cache import cache

@api_view(['GET'])
def EmployeeCategoryList(request):
    employee_category = cache.get('employee_category')
    if employee_category:
        print("cached_employee_category")
        return Response(employee_category)
    else:
        categories = EmployeeCategory.objects.all()
        serializer = EmployeeCategorySerializer(categories, many=True)
        cache.set('employee_category', serializer.data)
        print("db_employee_Category")
        return Response(serializer.data)


@api_view(['GET'])
def GetCoupons(request):
    coupon_codes = cache.get('coupon_code')
    if coupon_codes:
        print("cached_coupon")
        return Response(coupon_codes)
    else:
        coupons = CouponCode.objects.all()
        Serializer = CouponCodeSerializers(coupons, many=True)
        print("database_coupon")
        cache.set('coupon_code', Serializer.data)
        return Response(Serializer.data)
    
@api_view(['GET'])
def get_subcategory_for_single_category(request, id, slug):
    subcategory = cache.get(f"{slug}_subcategory")
    if subcategory:
        print(f"{slug}_category_cached")
        return Response(subcategory)
    else:
        subcategory = ServiceSubcategory.objects.filter(service_specialist__id=id, service_specialist__slug=slug)
        serializer = SubcategorySerializer(subcategory, many=True)
        cache.set(f"{slug}_subcategory", serializer.data)
        print(f"{slug}_category_db")
        return Response(serializer.data)

@api_view(['GET'])
def GetSubcategory(request):
    subcategory = ServiceSubcategory.objects.all()
    Serializer = SubcategorySerializer(subcategory, many=True)
    return Response(Serializer.data)

@api_view(['GET'])
def GetServices(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getEmployees(request, slug):
    print(request.user)
    employees = EmployeeCategory.objects.get(slug=slug).users.all()
    ser = UserSerializer(employees, many=True)
    return Response(ser.data)

@api_view(['GET'])
def getReviews(request, slug):
    employees = EmployeeCategory.objects.get(slug=slug).category_reviews.all().select_related('user', 'parent')
    ser = CategoryReviewSerializer(employees, many=True)
    return Response(ser.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createReview(request, slug):
    category = EmployeeCategory.objects.get(slug=slug)
    parent_id = request.data.get('parent', False)
    try:
        parent = CategoryReview.objects.get(id=parent_id)
    except CategoryReview.DoesNotExist:
        review = CategoryReview(star=request.data['star'], review=request.data['review'])
    else:
        review = CategoryReview(star=request.data['star'], review=request.data['review'], parent=parent)
    review.user = request.user
    review.category = category
    review.save()
    if parent_id:
        a = CategoryReview.objects.filter(category=category).select_related('user', 'parent')
        ser = CategoryReviewSerializer(a, many=True)
    else:
        ser = CategoryReviewSerializer(review)
    return Response(ser.data)

@api_view(['GET'])
def get_full_service(request, slug):
    all_service = ServiceSubcategory.objects.filter(service_specialist__slug=slug).prefetch_related('services')
    service_serializer = AllSubcategoryServiceSerializer(all_service, many=True)
    return Response(service_serializer.data)

