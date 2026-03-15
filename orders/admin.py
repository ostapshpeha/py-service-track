from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from orders.models import Order, Invoice, Part, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ["part"]


@admin.register(Part)
class PartAdmin(SimpleHistoryAdmin):
    """
    Operating parts via django-admin
    """

    list_display = (
        "sku",
        "name",
        "category",
        "stock_level",
        "purchase_price",
        "retail_price",
    )
    list_filter = ("category",)
    search_fields = ("sku", "name")
    ordering = ("name",)


@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):
    """
    Operating orders via django-admin
    """

    list_display = (
        "id",
        "client",
        "vehicle",
        "assigned_to",
        "mileage",
        "created_at",
        "status",
    )
    list_filter = ("status", "assigned_to", "client")
    search_fields = (
        "client__first_name",
        "client__last_name",
        "client__mobile_number",
        "vehicle__number_registration",
    )
    ordering = ("-created_at", "status")
    inlines = [OrderItemInline]


@admin.register(Invoice)
class InvoiceAdmin(SimpleHistoryAdmin):
    """
    Operating invoices via django-admin
    """

    list_display = ("id", "order", "labor_hours", "hourly_rate", "parts_total", "total")
    search_fields = ("order__client__first_name", "order__client__last_name")
    ordering = ("-id",)
