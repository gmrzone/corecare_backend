from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from django.core.mail import send_mail
from api.models import EmployeeCategory
from .utils import employee_document_location, profile_pic_loc

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validators = UnicodeUsernameValidator()
    
    number = models.CharField(max_length=10, db_index=True, unique=True)
    username = models.CharField(_('username'),max_length=150, null=True, blank=True, unique=True, validators=[username_validators], error_messages={'unique': _('A user with that username already exists.')})
    email = models.EmailField(_('email address'), unique=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    photo = models.ImageField(default='default-profile.png', upload_to=profile_pic_loc)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    document = models.ImageField(upload_to=employee_document_location, null=True, blank=True)
    is_verified_employee = models.BooleanField(default=False)
    employee_category = models.ForeignKey(EmployeeCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    date_joined = models.DateTimeField(default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message,from_email, [self.email], **kwargs)

    def get_full_name(self):
        full_name = f'{self.first_name} f{self.last_name}'
        return full_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.number

# Create your models here.
