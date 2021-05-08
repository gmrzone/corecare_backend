from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
app_name = "cart"

router = SimpleRouter()
router.register(r"orders", views.OrderViewSet, basename='orders')

urlpatterns = [
    path('cart/add/', views.add_service_to_cart, name="add_to_cart"),
    path('cart/remove/', views.remove_service_from_cart, name="remove_to_cart"),
    path('cart/get/detail/', views.get_cart, name="get_detail_cart"),
    path('cart/get/basic/', views.get_basic_cart, name="get_basic_cart"),
    path('cart/clear/', views.clear_cart, name="clear_cart"),
    path('cart/delete/', views.delete_service, name="delete_service"),
    path('coupon/apply/', views.apply_Coupon, name="apply_coupon"),
    path('create-razorpay-orders/', views.create_razorPay_order, name="create_rezorpay_order"),
    path('create-orders/', views.create_order, name="create_order"),
    path('services/get-recommandation/basic/', views.get_basic_recommandation, name="basic_recommandation"),
    path('services/get-recommandation/detail/', views.get_detailed_recommandation, name="detail_recommandation")
] + router.urls