from django.contrib.auth import get_user_model
from .models import CustomUser
from django.db import models
class NumberAuthentication:
    def authenticate(self, request, username, password):
        try:
            user = CustomUser.objects.get(number=username)
            if user.check_password(password):
                return user
            return None
        except CustomUser.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
           
           
