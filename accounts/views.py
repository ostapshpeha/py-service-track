from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import CustomUser
from crm.models import Client
from orders.models import Order


@login_required
def index(request):
    open_statuses = [
        Order.Status.IN_PROGRESS,
        Order.Status.NEEDS_CLARIFICATION,
    ]
    count_open_orders = Order.objects.filter(status__in=open_statuses).count()
    clients_without_vehicles = Client.objects.filter(vehicles__isnull=True).count()
    orders_without_invoices = Order.objects.filter(invoice__isnull=True)
    last_orders = Order.objects.order_by("-created_at")[:3]
    context = {
        "count_open_orders": count_open_orders,
        "clients_without_vehicles": clients_without_vehicles,
        "orders_without_invoices": orders_without_invoices,
        "last_orders": last_orders,
    }
    return render(request, "accounts/index.html", context)


class CustomUserListView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    success_url = reverse_lazy("accounts:staff-list")
