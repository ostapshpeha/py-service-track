from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from orders.models import Order, Invoice


@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):
    """
    Operating orders via django-admin
    """

    list_display = (
        "client",
        "vehicle",
        "requirements",
        "created_at",
        "status",
    )
    list_filter = ("status", "client")
    search_fields = (
        "client__first_name",
        "client__last_name",
        "client__mobile_number",
        "vehicle__number_registration",
    )
    ordering = ("-created_at", "status")


@admin.register(Invoice)
class InvoiceAdmin(SimpleHistoryAdmin):
    """
    Operating invoices via django-admin
    """

    list_display = ("id", "order", "total")
    search_fields = ("order__client__first_name", "order__client__last_name")
    ordering = ("-id",)
