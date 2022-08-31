from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "number",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "number",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        ("Required Fields", {"fields": ("number", "password")}),
        (
            _("Extra fields"),
            {"fields": ("username", "email", "first_name", "last_name", "photo")},
        ),
        (
            _("Employment_Detail"),
            {
                "fields": (
                    "employee_category",
                    "document",
                    "is_employee",
                    "is_verified_employee",
                )
            },
        ),
        (
            _("Address"),
            {"fields": ("address_1", "address_2", "city", "state", "pincode")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "verified",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "number",
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "employee_category",
                    "password1",
                    "password2",
                    "address_1",
                    "address_2",
                    "city",
                    "state",
                    "pincode",
                    "is_employee",
                    "is_verified_employee",
                    "verified",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("number", "email")
    ordering = ("-id",)


admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
