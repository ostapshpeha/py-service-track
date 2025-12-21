from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from orders.filters import OrderFilter
from orders.forms import OrderForm, InvoiceForm, InvoiceUpdateForm, OrderUpdateForm
from orders.models import Order, Invoice


class OrderListView(LoginRequiredMixin, FilterView):
    model = Order
    filterset_class = OrderFilter
    paginate_by = 30
    template_name = "orders/order_list.html"



class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:order-list")


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderUpdateForm
    success_url = reverse_lazy("orders:order-list")


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy("orders:order-list")


class InvoiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("orders:order-list")

    def get_initial(self):
        initial = super().get_initial()
        order_id = self.request.GET.get("order")
        if order_id:
            initial["order"] = Order.objects.get(pk=order_id)
        return initial


class InvoiceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Invoice
    form_class = InvoiceUpdateForm
    success_url = reverse_lazy("orders:invoice-list")
