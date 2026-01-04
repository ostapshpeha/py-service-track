from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
from crm.models import Client
from orders.models import Order


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Calculations for dashboard view
    Counting open orders to service
    Clients with 0 related vehicles
    Orders without invoices
    Last orders
    """
    template_name = "accounts/dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        open_statuses = [
            Order.Status.IN_PROGRESS,
            Order.Status.NEEDS_CLARIFICATION,
        ]

        context.update({
            "count_open_orders": Order.objects.filter(
                status__in=open_statuses
            ).count(),

            "clients_without_vehicles": Client.objects.filter(
                vehicles__isnull=True
            ).count(),

            "orders_without_invoices": Order.objects.filter(
                invoice__isnull=True
            ).select_related("client"),

            "last_orders": Order.objects.order_by("-created_at")[:3],
        })

        return context


class CustomUserListView(LoginRequiredMixin, generic.ListView):
    """
    Custom user list view
    """
    model = CustomUser


class ManagerRequiredMixin(UserPassesTestMixin):
    """
    Mixin to check if a user has required permissions
    """
    def test_func(self):
        user = self.request.user
        # Checking role for manager or superuser
        return user.is_authenticated and (
            user.role == CustomUser.Role.MANAGER or user.is_superuser
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                "Only admin or manager can perform this action."
            )
            return redirect("accounts:staff-list")

        return super().handle_no_permission()


class CustomUserCreateView(LoginRequiredMixin, ManagerRequiredMixin, generic.CreateView):
    """
    Creating new users, only by superadmin
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:staff-list")


class CustomUserUpdateView(LoginRequiredMixin, ManagerRequiredMixin, generic.UpdateView):
    """
    Updating users, only by superadmin
    """
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("accounts:staff-list")
