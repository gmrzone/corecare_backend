from django.contrib import admin
from django.db.models.query_utils import select_related_descend

from .models import Order, OrderItem

# Register your models here.


class OrderItemMInline(admin.StackedInline):
    model = OrderItem
    fields = ("service", "quantity", "total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "receipt",
        "coupon",
        "razorpay_order_id",
        "subtotal",
        "discount",
        "total",
        "paid",
        "status",
        "fullfill_by",
    )
    list_editable = ("paid", "status")
    list_filter = ("paid", "status")
    search_fields = ("status", "user")
    inlines = [OrderItemMInline]
    list_select_related = ("user", "coupon")

