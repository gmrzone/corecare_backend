from django.contrib import admin
from .models import EmployeeCategory, CouponCode, ServiceSubcategory, Service, CategoryReview
# Register your models here.
@admin.register(EmployeeCategory)
class EmployeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(CouponCode)
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active')
    list_editable = ('active', 'discount')
    list_filter = ('active', 'discount')

@admin.register(ServiceSubcategory)
class ServiceSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_specialist')
    list_filter = ('service_specialist',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'price', 'active')
    list_filter = ('active',)
    list_editable = ('price', 'active')
    search_fields = ('name',)
    
@admin.register(CategoryReview)
class CategoryReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'star', 'parent', 'created')
    list_filter = ('active', 'parent', 'star')
    list_editable = ('active', 'parent', 'star')