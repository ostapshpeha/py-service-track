from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Client, Vehicle


class VehicleInline(admin.TabularInline):
    """
    Vehicle tabular in line
    """
    model = Vehicle
    extra = 0
    fields = (
        "name", "number_registration", "vin_code",
        "engine_type", "last_service"
    )
    show_change_link = True


@admin.register(Client)
class ClientAdmin(SimpleHistoryAdmin):
    """
    Operating our clients with admin panel
    """
    list_display = (
        "id", "last_name", "first_name",
        "mobile_number", "vehicles_count"
    )
    search_fields = ("first_name", "last_name", "mobile_number")
    ordering = ("last_name", "first_name")
    inlines = (VehicleInline,)

    @admin.display(description="Vehicles")
    def vehicles_count(self, obj):
        return obj.vehicles.count()


@admin.register(Vehicle)
class VehicleAdmin(SimpleHistoryAdmin):
    """
    Operating vehicles with admin panel
    """
    list_display = (
        "id",
        "name",
        "number_registration",
        "vin_code",
        "engine_type",
        "client",
        "last_service",
    )
    list_filter = ("engine_type", "last_service")
    search_fields = (
        "name",
        "number_registration",
        "vin_code",
        "client__first_name",
        "client__last_name",
        "client__mobile_number",
    )
    ordering = ("name", "number_registration")
    autocomplete_fields = ("client",)
