from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from orders.forms import OrderForm, InvoiceForm
from orders.models import Order, Invoice


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 30
    context_object_name = "orders"


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:order-list")


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:order-list")


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy("orders:order-list")


class InvoiceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Invoice

    def get_object(self):
        return Invoice.objects.get(order_id=self.kwargs["pk"])


class InvoiceCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = InvoiceForm
    model = Invoice
    success_url = reverse_lazy("orders:invoice-list")


class InvoiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Invoice
    success_url = reverse_lazy("orders:invoice-list")


class InvoiceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("orders:invoice-list")
