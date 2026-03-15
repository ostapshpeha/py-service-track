from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
from crm.models import Client
from notes.models import Note
from orders.models import Order, Part


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Calculations for dashboard view
    Counting open orders to service
    Clients with 0 related vehicles
    Orders without invoices
    Last orders
    Low stock parts
    Recent notes
    Needs clarification orders
    Mechanic workload
    """

    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_statuses = [
            Order.Status.IN_PROGRESS,
            Order.Status.NEEDS_CLARIFICATION,
        ]

        context.update(
            {
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
                "low_stock_parts": Part.objects.filter(stock_level__lt=5).order_by(
                    "stock_level"
                )[:5],
                "recent_notes": Note.objects.select_related(
                    "author", "order__vehicle"
                ).order_by("-date")[:5],
                "needs_clarification_orders": Order.objects.filter(
                    status=Order.Status.NEEDS_CLARIFICATION
                ).select_related("client", "vehicle"),
                "mechanic_workload": CustomUser.objects.filter(
                    role=CustomUser.Role.MECHANIC
                )
                .annotate(
                    active_orders_count=Count(
                        "assigned_orders",
                        filter=Q(assigned_orders__status__in=open_statuses),
                    )
                )
                .order_by("-active_orders_count"),
            }
        )
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
                self.request, "Only admin or manager can perform this action."
            )
            return redirect("accounts:staff-list")

        return super().handle_no_permission()


class CustomUserCreateView(
    LoginRequiredMixin, ManagerRequiredMixin, generic.CreateView
):
    """
    Creating new users, only by superadmin
    """

    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:staff-list")


class CustomUserUpdateView(
    LoginRequiredMixin, ManagerRequiredMixin, generic.UpdateView
):
    """
    Updating users, only by superadmin
    """

    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("accounts:staff-list")
