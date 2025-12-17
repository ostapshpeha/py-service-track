from django.urls import path

from orders.views import (
    OrderListView, OrderDetailView,
    OrderCreateView, OrderUpdateView,
    OrderDeleteView, InvoiceListView,
    InvoiceDetailView, InvoiceCreateView,
    InvoiceDeleteView, InvoiceUpdateView
)

app_name = "orders"

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order-update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order-delete"),
    path("invoices/", InvoiceListView.as_view(), name="invoice-list"),
    path(
        "invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice-detail"
    ),
    path("invoices/create/", InvoiceCreateView.as_view(), name="invoice-create"),
    path(
        "invoices/<int:pk>/delete/",
        InvoiceDeleteView.as_view(),
        name="invoice-delete"
    ),
    path(
        "invoices/<int:pk>/update/",
        InvoiceUpdateView.as_view(),
        name="invoice-update"
    ),
]