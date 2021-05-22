from django.urls import path
from . import views
from . import viewsets
from rest_framework.routers import SimpleRouter
app_name = "cart"

router = SimpleRouter()
router.register(r"orders", viewsets.OrderViewSet, basename='orders')
urlpatterns = [
    path('cart/add/', views.AddServiceToCart.as_view(), name="add_to_cart"),
    path('cart/remove/', views.RemoveServiceFromCart.as_view(), name="remove_to_cart"),
    path('cart/get/detail/', views.get_cart, name="get_detail_cart"),
    path('cart/get/basic/', views.get_basic_cart, name="get_basic_cart"),
    path('cart/clear/', views.clear_cart, name="clear_cart"),
    path('cart/delete/', views.DeleteService.as_view(), name="delete_service"),
    path('coupon/apply/', views.apply_Coupon, name="apply_coupon"),
    path('create-razorpay-orders/', views.CreateRazorPayOrder.as_view(), name="create_rezorpay_order"),
    path('create-orders/', views.create_order, name="create_order"),
    path('services/get-recommandation/basic/', views.get_basic_recommandation, name="basic_recommandation"),
    path('services/get-recommandation/detail/', views.get_detailed_recommandation, name="detail_recommandation"),
    path('cart/add/from_recommanded/', views.add_from_recommanded_toCart, name="add_from_recommanded"),
    path('order/invoice/generate/download/<str:order_id>/', views.download_pdf, name="download_invoice"),

    # New ENDPOINTS VERSIONS
    path('create-orders/', views.CreateOrder.as_view(), name="create_order_new"),
] + router.urls