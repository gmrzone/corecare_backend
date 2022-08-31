import os
from datetime import datetime

from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck
from rest_framework_simplejwt.tokens import RefreshToken


def employee_document_location(instance, filename):
    path = os.path.join("Employee_Documents", instance.number, filename)
    return path


def profile_pic_loc(instance, filename):
    path = os.path.join("Users_Profile_pic", instance.number, filename)
    return path


def validate_number(number):
    if number:
        return True
    else:
        return False


def generate_key_for_otp(number):
    return str(number) + str(datetime.date(datetime.now())) + "corecareservices"


# Http Only Cookie

# TODO WORKAROUND NEED TO FIX THIS PERMANENTLY
def dummy_get_response(request):  # pragma: no cover
    return None

def enforce_csrf(request):
    csrf_check = CSRFCheck(dummy_get_response)
    csrf_check.process_request(request)
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    reason = csrf_check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        msg = f"CSRF FAILED {reason}"
        raise exceptions.PermissionDenied(msg)


def get_token(user):
    token = RefreshToken.for_user(user)
    return {
        "refresh": str(token),
        "access": str(token.access_token),
    }


def timedelta_to_second(timedelta):
    seconds = timedelta.seconds
    if not seconds:
        seconds = timedelta.days * 3600 * 24
    return seconds
