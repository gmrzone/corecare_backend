from django.core.exceptions import ValidationError
import re


def number_validator(value):
    error = False if re.match("^[789]\d{9}$", value) else True
    if error:
        raise ValidationError("Invalid Number")
