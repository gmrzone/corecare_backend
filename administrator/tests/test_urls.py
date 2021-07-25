from django.test import TestCase
from django.urls import resolve, reverse
from ..views import *


class UrlTests(TestCase):

    def test_all_users_url(self):
        url = reverse('administrator:all_users')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetUsers)

    def test_create_users_url(self):
        url = reverse('administrator:create_user')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateUser)

    def test_all_employees_url(self):
        url = reverse('administrator:all_employees')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetEmployees)

    def test_create_employees_url(self):
        url = reverse('administrator:create_employee')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateEmployee)

    def test_all_orders_url(self):
        url = reverse('administrator:all_orders')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetOrders)

    def test_create_orders_url(self):
        url = reverse('administrator:create_order')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateOrder)

    def test_all_subcategory_url(self):
        url = reverse('administrator:all_subcategories')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetSubCategories)

    def test_create_subcategory_url(self):
        url = reverse('administrator:create_subcategory')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateSubCategory)

    def test_all_service_url(self):
        url = reverse('administrator:all_services')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, GetServices)

    def test_create_service_url(self):
        url = reverse('administrator:create_service')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CreateService)

