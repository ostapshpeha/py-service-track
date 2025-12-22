from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic
from django_filters.views import FilterView

from orders.filters import OrderFilter
from orders.forms import (
    OrderForm, InvoiceForm, InvoiceUpdateForm,
    OrderUpdateForm, OrderClientLastNameSearchForm
)
from orders.models import Order, Invoice


class OrderListView(LoginRequiredMixin, FilterView):
    """
    Order list view with searching by last name of the client
    and filtering
    """
    model = Order
    filterset_class = OrderFilter
    paginate_by = 30
    template_name = "orders/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = OrderClientLastNameSearchForm(
            self.request.GET or None
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = OrderClientLastNameSearchForm(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data["q"]
            if q:
                queryset = queryset.filter(
                    client__last_name__icontains=q
                )

        return queryset


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Order detail view
    """
    model = Order


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Order create view, redirect to detail view
    """
    model = Order
    form_class = OrderForm

    def get_success_url(self):
        return reverse(
            "orders:order-detail",
            kwargs={"pk": self.object.pk}
        )


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Order update view, redirect to detail view
    """
    model = Order
    form_class = OrderUpdateForm

    def get_success_url(self):
        return reverse(
            "orders:order-detail",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Order delete view
    """
    model = Order
    success_url = reverse_lazy("orders:order-list")


class InvoiceCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Invoice create view
    An invoice can only be created once and only through the order page
    You can only view the short invoice through the order page
    """
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse(
            "orders:order-detail",
            kwargs={"pk": self.object.pk}
        )

    def get_initial(self):
        """
        Automatically link the invoice and the order to each other
        """
        initial = super().get_initial()
        order_id = self.request.GET.get("order")
        if order_id:
            initial["order"] = Order.objects.get(pk=order_id)
        return initial


class InvoiceUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Invoice update view redirect to order detail
    """
    model = Invoice
    form_class = InvoiceUpdateForm

    def get_success_url(self):
        return reverse(
            "orders:order-detail",
            kwargs={"pk": self.object.pk}
        )
