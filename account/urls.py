from django.urls import path
from .views import get_current_user

urlpatterns = [
    path('get_current_user/', get_current_user, name="get_current_user"),
]