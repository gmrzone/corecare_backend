from django.urls import path

from .views import *

app_name = "administrator"


urlpatterns = [
    path("get-all-user/", GetUsers.as_view(), name="all_users"),
    path("get-all-employees/", GetEmployees.as_view(), name="all_employees"),
    path("get-orders/", GetOrders.as_view(), name="all_orders"),
    path("get-subcategories/", GetSubCategories.as_view(), name="all_subcategories"),
    path("get-services/", GetServices.as_view(), name="all_services"),
    path("get-blog-posts/", GetBlogPosts.as_view(), name="all_posts"),
    path("get-comments/", GetBlogPostComments.as_view(), name="all_comments"),
    path("get_coupons/", GetCoupons.as_view(), name="all_coupons"),
    path("create-user/", CreateUser.as_view(), name="create_user"),
    path("create-employee/", CreateEmployee.as_view(), name="create_employee"),
    path("create-order/", CreateOrder.as_view(), name="create_order"),
    path("create-subcategory/", CreateSubCategory.as_view(), name="create_subcategory"),
    path("login/", AdminLogin.as_view(), name="login"),
    path("get-current-user/", GetCurrentUser.as_view(), name="get_current_user"),
    path("create-service/", CreateService.as_view(), name="create_service"),
    path("create_post/", CreateBlogPost.as_view(), name="create_post"),
    path("create_comments/", CreateBlogPostComment.as_view(), name="create_comments"),
    path("create_coupon/", CreateCoupon.as_view(), name="create_coupon"),
    path("get-user/<str:number>/<int:pk>/", GetUser.as_view(), name="get_user"),
    path(
        "get-employee/<str:number>/<int:pk>/",
        GetEmployee.as_view(),
        name="get_employee",
    ),
    path("get-order/<str:receipt>/<int:pk>/", GetOrder.as_view(), name="get_order"),
    path(
        "get-subcategory/<slug:slug>/<int:pk>/",
        GetSubcategory.as_view(),
        name="get_subcategory",
    ),
    path(
        "get-service/<int:created__year>/<int:created__month>/<int:pk>/",
        GetService.as_view(),
        name="get_service",
    ),
    path(
        "get-blog-post/<int:created__year>/<int:created__month>/<int:created__day>/<slug:slug>/",
        GetBlogPost.as_view(),
        name="get_blog_post",
    ),
    path(
        "get-comment/<int:created__year>/<int:created__month>/<int:created__day>/<int:pk>/",
        GetBlogPostComment.as_view(),
        name="get_comment",
    ),
    path(
        "get-coupon/<str:code>/<int:pk>/",
        GetCoupon.as_view(),
        name="get_coupon",
    ),
]
