
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from .utils import enforce_csrf
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken


class CustomAuthentication(JWTAuthentication):

    def authenticate(self, request):
        
        header = self.get_header(request)
        # if header is none that means no bearer token is provided by frontend
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE', None), None)
            # refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', None), None)           
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', None), None)
            if refresh_token:
                refresh = RefreshToken(refresh_token)
                raw_token = str(refresh.access_token)
            else:
                return None
        validated_token = self.get_validated_token(raw_token)

        enforce_csrf(request)
        return self.get_user(validated_token), validated_token


           
           
