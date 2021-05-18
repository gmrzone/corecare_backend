
# Rest framework import
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
# Models Import
from .models import CategoryReview, EmployeeCategory, CouponCode, Service, ServiceSubcategory

# Serializers import
from .serializers import CouponCodeSerializers, EmployeeCategorySerializer, SubcategorySerializer, ServiceSerializer, CategoryReviewSerializer, AllSubcategoryServiceSerializer, ContactSerializer, PartnerRequestSerializer
from account.serializers import UserSerializer

# Others imports
from itertools import chain

# Django Imports
from django.core.cache import cache
from django.core.mail import send_mail, mail_admins


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
        return Response(coupon_codes)
    else:
        coupons = CouponCode.objects.all().prefetch_related('category')
        Serializer = CouponCodeSerializers(coupons, many=True)
        cache.set('coupon_code', Serializer.data)
        return Response(Serializer.data)
    
@api_view(['GET'])
def get_subcategory_for_single_category(request, id, slug):
    subcategory = cache.get(f"{slug}_subcategory")
    if subcategory:
        return Response(subcategory)
    else:
        subcategory = ServiceSubcategory.objects.filter(service_specialist__id=id, service_specialist__slug=slug).select_related('service_specialist')
        serializer = SubcategorySerializer(subcategory, many=True)
        cache.set(f"{slug}_subcategory", serializer.data)
        print(f"{slug}_category_db")
        return Response(serializer.data)

@api_view(['GET'])
def GetSubcategory(request):
    subcategory = ServiceSubcategory.objects.all().select_related('service_specialist')
    Serializer = SubcategorySerializer(subcategory, many=True)
    return Response(Serializer.data)

@api_view(['GET'])
def GetServices(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getEmployees(request, slug):
    employees = EmployeeCategory.objects.get(slug=slug).users.all()
    ser = UserSerializer(employees, many=True)
    return Response(ser.data)

@api_view(['GET'])
def getReviews(request, slug):
    # employees = EmployeeCategory.objects.get(slug=slug).category_reviews.all().select_related('user', 'parent')
    reviews = CategoryReview.objects.filter(category__slug=slug).select_related('parent', 'user').prefetch_related('replies')
    ser = CategoryReviewSerializer(reviews, many=True)
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
    
@api_view(['GET'])
def search_service(request, query, city):
    if (query):
        service_sub = ServiceSubcategory.objects.filter(name__icontains=query).select_related('service_specialist')
        data = SubcategorySerializer(service_sub, many=True).data
    else:
        data = []
    return Response(data)

@api_view(['GET'])
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
                mail_subject = "CoreCare Contact Us"
                mail_message = f"""A Contact Message from
                Name: {data['first_name']} {data['last_name']}
                email : {data['email']}
                message: {data['message']}"""
                success_msg = "Thank you for contacting us. we Will get back to you as soon as possible"
            elif self.type == "partner":
                mail_subject = "CoreCare Partner Request"
                mail_message = f"""
                Name: {data['name']}
                Number: {data['number']}
                email : {data['email']}
                detail: {data['detail']}"""
                success_msg = "Thank you for showing Interest in CoreCare Partners. we Will get back to you as soon as possible"
            try:
                # mail_admins(mail_subject, mail_message, fail_silently=False)
                send_mail(mail_subject, mail_message,'saiyedafzal0@gmail.com',['saiyedafzalgz@gmail.com'])
            except Exception as e:
                return Response({'status': 'error', 'message': "There was an error on our end please try again later."})
            else:
                instance.save()
                return Response({'status': 'ok', 'message': success_msg})
        else:
            return Response({'status': 'error', 'message': "Please Make sure that your imformation is accurate or try again later"})


class CreatePartnerRequest(SendContactAndPartnerMixin, CreateAPIView):
    serializer_class = PartnerRequestSerializer
    type = "partner"

class ContactUs(SendContactAndPartnerMixin, CreateAPIView):
    serializer_class = ContactSerializer
    type = 'contact'

# @api_view(['POST'])
# def partner_request(request):
#     data = request.data
#     instance = PartnerRequestSerializer(data=data)
#     if instance.is_valid():
#         mail_subject = "CoreCare Partner Request"
#         mail_message = f"""
#         Name: {data['name']}
#         Number: {data['number']}
#         email : {data['email']}
#         detail: {data['detail']}"""
#         try:
#             # mail_admins(mail_subject, mail_message, fail_silently=False)
#             send_mail(mail_subject, mail_message,'saiyedafzal0@gmail.com',['saiyedafzalgz@gmail.com'])
#         except Exception as e:
#             return Response({'status': 'error', 'message': "There was an error on our end please try again later."})
#         else:
#             instance.save()
#             return Response({'status': 'ok', 'message': "Thank you for showing Interest in CoreCare Partners. we Will get back to you as soon as possible"})
#     else:
#         return Response({'status': 'error', 'message': "Please Make sure that your imformation is accurate or try again later"})

# class CreatePartnerRequest(CreateAPIView):
#     serializer_class = PartnerRequestSerializer
    
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         instance = self.serializer_class(data=data)
#         if instance.is_valid():
#             mail_subject = "CoreCare Partner Request"
#             mail_message = f"""
#             Name: {data['name']}
#             Number: {data['number']}
#             email : {data['email']}
#             detail: {data['detail']}"""
#             try:
#                 # mail_admins(mail_subject, mail_message, fail_silently=False)
#                 send_mail(mail_subject, mail_message,'saiyedafzal0@gmail.com',['saiyedafzalgz@gmail.com'])
#             except Exception as e:
#                 return Response({'status': 'error', 'message': "There was an error on our end please try again later."})
#             else:
#                 instance.save()
#                 return Response({'status': 'ok', 'message': "Thank you for showing Interest in CoreCare Partners. we Will get back to you as soon as possible"})
#         else:
#             return Response({'status': 'error', 'message': "Please Make sure that your imformation is accurate or try again later"})

# @api_view(['POST'])
# def contact_us(request):
#     data = request.data
#     instance = ContactSerializer(data=data)
#     if instance.is_valid():
#         mail_subject = "CoreCare ContactUs"
#         mail_message = f"""A Contact Message from
#         Name: {data['first_name']} {data['last_name']}
#         email : {data['email']}
#         message: {data['message']}"""
#         try:
#             # mail_admins(mail_subject, mail_message, fail_silently=False)
#             send_mail(mail_subject, mail_message,'saiyedafzal0@gmail.com',['saiyedafzalgz@gmail.com'])
#         except Exception as e:
#             return Response({'status': 'error', 'message': "There was an error on our end please try again later."})
#         else:
#             instance.save()
#             return Response({'status': 'ok', 'message': "Thank you for contacting us. we Will get back to you as soon as possible"})
#     else:
#         return Response({'status': 'error', 'message': "Please Make sure that your imformation is accurate or try again later"})

# class ContactUs(CreateAPIView):
#     serializer_class = ContactSerializer

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         instance = self.serializer_class(data=request.data)
#         if instance.is_valid():
#             mail_subject = "CoreCare ContactUs"
#             mail_message = f"""A Contact Message from
#             Name: {data['first_name']} {data['last_name']}
#             email : {data['email']}
#             message: {data['message']}"""
#             try:
#                 # mail_admins(mail_subject, mail_message, fail_silently=False)
#                 send_mail(mail_subject, mail_message,'saiyedafzal0@gmail.com',['saiyedafzalgz@gmail.com'])
#             except Exception as e:
#                 return Response({'status': 'error', 'message': "There was an error on our end please try again later."})
#             else:
#                 instance.save()
#                 return Response({'status': 'ok', 'message': "Thank you for contacting us. we Will get back to you as soon as possible"})
#         else:
#             return Response({'status': 'error', 'message': "Please Make sure that your imformation is accurate or try again later"})