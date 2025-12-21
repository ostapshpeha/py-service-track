from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import WorkerCreationForm, WorkerChangeForm
from .models import Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    """
    Custom admin panel to interact with our staff's accounts
    """
    add_form = WorkerCreationForm
    form = WorkerChangeForm
    model = Worker

    list_display = ("username", "first_name", "last_name", "role", "mechanic_position", "is_staff", "is_superuser")
    list_filter = ("role", "mechanic_position", "is_staff", "is_superuser", "is_active")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Track Service", {"fields": ("role", "mechanic_position")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Track Service", {"fields": ("role", "mechanic_position")}),
    )

