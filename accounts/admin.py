from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "username",
        "first_name",
        "last_name",
        "role",
        "mechanic_position",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("role", "mechanic_position", "is_staff", "is_superuser", "is_active")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Track Service", {"fields": ("role", "mechanic_position")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Track Service", {"fields": ("role", "mechanic_position")}),
    )
