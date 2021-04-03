from django.urls import path
from django.http import HttpResponse
from . import views
app_name = 'api'


urlpatterns = [
    path('', views.EmployeeCategoryList, name='employee_category_list'),
    path('coupons/', views.GetCoupons, name='coupon_list'),
    path('subcategory/', views.GetSubcategory, name='subcategory'),
    path('services/', views.GetServices, name='services_list'),
    path('subcategory/<int:id>/<slug:slug>/', views.get_subcategory_for_single_category, name="get_subcategory_for_single_category"),
    path('get_employee/<slug:slug>/', views.getEmployees, name="get_employee"),
    path('get_reviews/<slug:slug>/', views.getReviews, name="get_reviews"),
    path('create_review/<slug:slug>/new/', views.createReview, name="create_review"),
    path('get_services/<slug:slug>/', views.get_full_service, name="get_full_service"),
    path('contact/send/', views.contact_us, name="contact_us"),
    path('search/<str:query>/<str:city>/', views.search_service, name="search_service")
]   