from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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

