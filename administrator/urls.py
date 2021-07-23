from django.urls import path

from .views import *

app_name = "administrator"


urlpatterns = [
    path("get-all-user/", GetUsers.as_view(), name="all_users"),
    path("get-all-employees/", GetEmployees.as_view(), name="all_employees"),
    path("get-orders/", GetOrders.as_view(), name="all_orders"),
    path("get-category/", GetCategories.as_view(), name="all_categories"),
    path("get-services/", GetServices.as_view(), name="all_services"),
    path("get-blog-posts/", GetBlogPosts.as_view(), name="all_posts"),
    path("get-comments/", GetBlogPostComments.as_view(), name="all_comments"),
    path("get_coupons/", GetCoupons.as_view(), name="all_coupons"),
    path("create-user/", CreateUser.as_view(), name="create_user"),
    path("create-employee/", CreateEmployee.as_view(), name="create_employee"),
    path("create-order/", CreateOrder.as_view(), name="create_order"),
]
