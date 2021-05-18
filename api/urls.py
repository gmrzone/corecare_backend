from django.urls import path
from django.http import HttpResponse
from . import views
app_name = 'api'


urlpatterns = [
    
    path('', views.EmployeeCategoryList, name='employee_category_list'),
    # path('', views.afzal, name='employee_category_list'),
    path('coupons/', views.GetCouponsView.as_view(), name='coupon_list'),
    path('subcategory/', views.GetSubcategory, name='subcategory'),
    path('services/', views.GetServices, name='services_list'),
    path('services/v2/', views.GetServiceList.as_view(), name='services_list_new'),
    path('subcategory/<int:id>/<slug:slug>/', views.get_subcategory_for_single_category, name="get_subcategory_for_single_category"),
    path('get_employee/<slug:slug>/', views.getEmployees, name="get_employee"),
    path('get_reviews/<slug:slug>/', views.getReviews, name="get_reviews"),
    path('create_review/<slug:slug>/new/', views.createReview, name="create_review"),
    path('get_services/<slug:slug>/', views.get_full_service, name="get_full_service"),
    path('search/<str:query>/<str:city>/', views.search_service, name="search_service"),
    path('category/hiring/', views.getHiringEmployeeCategories, name="hiring_category"),
    path('partner/request/', views.CreatePartnerRequest.as_view(), name="partner_request"),
    path('contact/send/', views.ContactUs.as_view(), name="contact_us"),
]   