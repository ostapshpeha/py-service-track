from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from orders.models import Order


@login_required
def index(request):
    open_statuses = [
        Order.Status.IN_PROGRESS,
        Order.Status.NEEDS_CLARIFICATION,
    ]
    count_open_orders = Order.objects.filter(status__in=open_statuses).count()
    list_open_orders = Order.objects.filter(status__in=open_statuses)
    orders_without_invoices = Order.objects.filter(invoice__isnull=True)
    context = {
        "count_open_orders": count_open_orders,
        "list_open_orders": list_open_orders,
        "orders_without_invoices": orders_without_invoices,
    }
    return render(request, "accounts/index.html", context)

