from django.urls import path
from .views import get_current_user, signup, verify_otp, signup_additional, update_profile_image

urlpatterns = [
    path('get_current_user/', get_current_user, name="get_current_user"),
    path('create_user_account/', signup, name="create_user_account"),
    path('create_user_account/additional/', signup_additional, name="additional_fields"),
    path('create_user_account/verify/', verify_otp, name="verify_otp"),
    path('create_user_account/profile-image/', update_profile_image, name="update_profile_image"),
]