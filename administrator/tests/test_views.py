from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.


class AdminLoginTests(TestCase):

    # Create 2 users one normal and one admin
    def setUp(self) -> None:
        self.model = get_user_model()
        self.normal_user_number = "7286444556"
        self.normal_user_password = 'normal_user_password'
        self.admin_user_number = "7894563214"
        self.admin_user_password = 'admin_user_password'
        normal_user = self.model(number=self.normal_user_number, email="testemail@gmail.com", username="normal_user", is_active=True)
        normal_user.set_password(self.normal_user_password)
        normal_user.save()
        admin_user = self.model(number=self.admin_user_number, email="testemail1@gmail.com", username="admin_user", is_active=True, is_staff=True, is_superuser=True)
        admin_user.set_password(self.admin_user_password)
        admin_user.save()

    # total user create is 2
    def test_user_creation(self):
        self.assertEqual(self.model.objects.all().count(), 2)

    # Normal users should not be able to login so status should be 400
    def test_normal_user_login(self):
        url = reverse('administrator:login')
        response = self.client.post(url, data={'number': self.normal_user_number, "password": self.normal_user_password})
        self.assertEquals(response.status_code, 400)

    # Admin users should not be able to login so status should be 200
    def test_admin_user_login(self):
        url = reverse('administrator:login')
        response = self.client.post(url, data={'number': self.admin_user_number, "password": self.admin_user_password})
        self.assertEquals(response.status_code, 200)
