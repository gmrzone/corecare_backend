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
    path('subcategory/<int:id>/<slug:slug>/', views.get_subcategory_for_single_category, name="get_subcategory_for_single_category"),
    path('get_employee/<slug:slug>/', views.getEmployees, name="get_employee"),
    path('get_reviews/<slug:slug>/', views.getReviews, name="get_reviews"),
    path('create_review/<slug:slug>/new/', views.createReview, name="create_review"),
    path('get_services/<slug:slug>/', views.get_full_service, name="get_full_service"),
    path('search/<str:query>/<str:city>/', views.search_service, name="search_service"),
    path('category/hiring/', views.getHiringEmployeeCategories, name="hiring_category"),
    path('partner/request/', views.CreatePartnerRequest.as_view(), name="partner_request"),
    path('contact/send/', views.ContactUs.as_view(), name="contact_us"),

    # New Version Endpoints V2
    path('subcategory/v2/<int:id>/<slug:slug>/', views.GetSubcategoryForSingleCategory.as_view(), name="get_subcategory_for_single_category_new"),
    path('get_employee/v2/<slug:slug>/', views.GetEmployeesList.as_view(), name="get_employee_new"),
    path('get_services/v2/<slug:slug>/', views.GetFullServiceList.as_view(), name="get_full_service_new"),
    path('get_reviews/v2/<slug:slug>/', views.GetReviewsList.as_view(), name="get_reviews_new"),
    path('category/v2/hiring/', views.GetHiringEmployeeCategory.as_view(), name="hiring_category_new"),
    path('search/v2/<str:query>/<str:city>/', views.SearchServices.as_view(), name="search_service_new"),

    path('v2/', views.EmployeeCategoryListView.as_view(), name='employee_category_list_new'),
    path('subcategory/v2/', views.GetSubcategoryView.as_view(), name='subcategory_new'),
    path('services/v2/', views.GetServiceList.as_view(), name='services_list_new'),


]   