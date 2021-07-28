from django.test import TestCase
from django.urls import resolve, reverse

from ..views import *


class ListUrlTests(TestCase):
    def test_users_list_url(self):
        url = reverse("administrator:all_users")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetUsers)

    def test_employees_list_url(self):
        url = reverse("administrator:all_employees")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetEmployees)

    def test_orders_list_url(self):
        url = reverse("administrator:all_orders")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetOrders)

    def test_subcategory_list_url(self):
        url = reverse("administrator:all_subcategories")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetSubCategories)

    def test_service_list_url(self):
        url = reverse("administrator:all_services")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetServices)

    def test_post_list_url(self):
        url = reverse("administrator:all_posts")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetBlogPosts)

    def test_comment_list_url(self):
        url = reverse("administrator:all_comments")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetBlogPostComments)

    def test_coupon_list_url(self):
        url = reverse("administrator:all_coupons")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetCoupons)

    def test_create_coupon_url(self):
        url = reverse("administrator:create_coupon")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateCoupon)


class RetriveUrlTest(TestCase):
    def test_user_detail_url(self):
        url = reverse(
            "administrator:get_user", kwargs={"number": "7208333993", "pk": 1}
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetUser)

    def test_employee_detail_url(self):
        url = reverse(
            "administrator:get_employee", kwargs={"number": "7208333993", "pk": 1}
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetEmployee)

    def test_order_detail_url(self):
        url = reverse(
            "administrator:get_order", kwargs={"receipt": "ORD123456789", "pk": 1}
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetOrder)

    def test_subcategory_detail_url(self):
        url = reverse(
            "administrator:get_subcategory", kwargs={"slug": "fffff", "pk": 1}
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetSubcategory)

    def test_service_detail_url(self):
        url = reverse(
            "administrator:get_service",
            kwargs={"created__year": 2021, "created__month": 2, "pk": 1},
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetService)

    def test_post_detail_url(self):
        url = reverse(
            "administrator:get_blog_post",
            kwargs={
                "created__year": 2021,
                "created__month": 2,
                "created__day": 3,
                "slug": "aff",
            },
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetBlogPost)

    def test_comment_detail_url(self):
        url = reverse(
            "administrator:get_comment",
            kwargs={
                "created__year": 2021,
                "created__month": 2,
                "created__day": 3,
                "pk": 1,
            },
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetBlogPostComment)

    def test_coupon_detail_url(self):
        url = reverse(
            "administrator:get_coupon",
            kwargs={"code": "COUPON_CODE", "pk": 1},
        )
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetCoupon)


class CreateUrlTests(TestCase):
    def test_create_users_url(self):
        url = reverse("administrator:create_user")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateUser)

    def test_create_employees_url(self):
        url = reverse("administrator:create_employee")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateEmployee)

    def test_create_orders_url(self):
        url = reverse("administrator:create_order")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateOrder)

    def test_create_subcategory_url(self):
        url = reverse("administrator:create_subcategory")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateSubCategory)

    def test_create_service_url(self):
        url = reverse("administrator:create_service")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateService)

    def test_create_post_url(self):
        url = reverse("administrator:create_post")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateBlogPost)

    def test_create_coupon_url(self):
        url = reverse("administrator:create_coupon")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateCoupon)


class UpdateUrlTests(TestCase):

    def test_update_user(self):
        url = reverse('administrator:update_user', kwargs={"number": "7208333993", "pk": 1})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, UpdateUser)

    def test_update_user(self):
        url = reverse('administrator:update_employee', kwargs={"number": "7208333993", "pk": 1})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, UpdateEmployee)

    def test_update_order(self):
        url = reverse('administrator:update_order', kwargs={"receipt": "ORD146694dd", "pk": 1})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, UpdateOrder)


class DeleteUrlTest(TestCase):

    def test_delete_user(self):
        url = reverse('administrator:delete_user', kwargs={"number": "7208333993", "pk": 1})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, DeleteUser)






