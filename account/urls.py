from django.urls import path
from rest_framework import routers
from .views import signup_additional, update_profile_image
from .views import SignUp, GetCurrentUser, UpdateSignupAdditionalData, VerifyOtp, UpdateProfileImage, LoginView
from rest_framework.routers import DefaultRouter

app_name = 'account'


urlpatterns = [
    path('get_current_user/', GetCurrentUser.as_view(), name="get_current_user"),
    path('create_user_account/', SignUp.as_view(), name="create_user_account"),
    path('create_user_account/additional/', signup_additional, name="additional_fields"),
    path('create_user_account/verify/', VerifyOtp.as_view(), name="verify_otp"),
    path('create_user_account/profile-image/', update_profile_image, name="update_profile_image"),

    # New Endpoints V2
    path('create_user_account/additional/v2/<str:number>/', UpdateSignupAdditionalData.as_view(), name="additional_data"),
    path('create_user_account/profile-image/v2/<str:number>/', UpdateProfileImage.as_view(), name="update_profile_image_new"),
    path('login/v1/', LoginView.as_view(), name="new_login_view")

]