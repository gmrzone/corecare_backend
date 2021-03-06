from django.contrib import admin

from .models import (CategoryReview, Contact, CouponCode, EmployeeCategory,
                     PartnerRequest, Service, ServiceSubcategory)


# Register your models here.
@admin.register(EmployeeCategory)
class EmployeeCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(CouponCode)
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "active")
    list_editable = ("active", "discount")
    list_filter = ("active", "discount")


@admin.register(ServiceSubcategory)
class ServiceSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "service_specialist")
    list_filter = ("service_specialist",)
    list_select_related = ("service_specialist",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory", "price", "active")
    list_filter = ("active",)
    list_editable = ("price", "active")
    search_fields = ("name",)
    list_select_related = ("subcategory",)


@admin.register(CategoryReview)
class CategoryReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "active", "star", "parent", "created")
    list_filter = ("active", "parent", "star")
    list_editable = ("active", "parent", "star")


@admin.register(Contact)
class ContAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    list_filter = ("email", "created")
    list_editable = ("email",)
    search_fields = ("email", "first_name")


@admin.register(PartnerRequest)
class PartnerRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "number", "detail")
    list_filter = ("email",)
    list_editable = ("email",)
    search_field = ("name", "email", "number")
