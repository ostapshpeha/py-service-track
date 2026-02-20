from django.urls import path

from orders.views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    InvoiceUpdateView,
    InvoiceCreateView,
)

app_name = "orders"

urlpatterns = [
    path("list/", OrderListView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("<int:pk>/update/", OrderUpdateView.as_view(), name="order-update"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order-delete"),
    path(
        "<int:pk>/invoice/create/", InvoiceCreateView.as_view(), name="invoice-create"
    ),
    path(
        "<int:pk>/invoice/update/", InvoiceUpdateView.as_view(), name="invoice-update"
    ),
]
