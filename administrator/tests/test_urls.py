from django.test import TestCase
from django.urls import resolve, reverse

from ..views import *


class UrlTests(TestCase):
    def test_users_list_url(self):
        url = reverse("administrator:all_users")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetUsers)

    def test_create_users_url(self):
        url = reverse("administrator:create_user")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateUser)

    def test_employees_list_url(self):
        url = reverse("administrator:all_employees")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetEmployees)

    def test_create_employees_url(self):
        url = reverse("administrator:create_employee")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateEmployee)

    def test_orders_list_url(self):
        url = reverse("administrator:all_orders")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetOrders)

    def test_create_orders_url(self):
        url = reverse("administrator:create_order")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateOrder)

    def test_subcategory_list_url(self):
        url = reverse("administrator:all_subcategories")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetSubCategories)

    def test_create_subcategory_url(self):
        url = reverse("administrator:create_subcategory")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateSubCategory)

    def test_service_list_url(self):
        url = reverse("administrator:all_services")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetServices)

    def test_create_service_url(self):
        url = reverse("administrator:create_service")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateService)

    def test_post_list_url(self):
        url = reverse("administrator:all_posts")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetBlogPosts)

    def test_create_post_url(self):
        url = reverse("administrator:create_post")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateBlogPost)

    def test_comment_list_url(self):
        url = reverse("administrator:all_comments")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetBlogPostComments)

    def test_create_comment_url(self):
        url = reverse('administrator:create_comments')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateBlogPostComment)

    def test_coupon_list_url(self):
        url = reverse("administrator:all_coupons")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetCoupons)

    def test_create_coupon_url(self):
        url = reverse('administrator:create_coupon')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateCoupon)
