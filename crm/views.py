from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Max
from django.urls import reverse_lazy, reverse
from django.views import generic

from crm.forms import (
    ClientForm, VehicleForm, VehicleUpdateForm,
    ClientLastNameSearchForm, VehicleNumberSearchForm
)
from crm.models import Vehicle, Client


class VehicleListView(LoginRequiredMixin, generic.ListView):
    """
    Vehicle list view with last service ordering
    Searching through the vehicle number of registration
    """
    model = Vehicle
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = VehicleNumberSearchForm(
            self.request.GET or None
        )
        return context

    def get_queryset(self):
        queryset = Vehicle.objects.all().order_by("-last_service")
        form = VehicleNumberSearchForm(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data["q"]
            if q:
                queryset = queryset.filter(
                    number_registration__icontains=q
                )

        return queryset.select_related("client").prefetch_related("orders")


class VehicleDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Vehicle detail view
    """
    model = Vehicle

    def get_queryset(self):
        return super().get_queryset().select_related("client").prefetch_related("notes", "orders")


class VehicleCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Vehicle create view, redirects to DetailView template
    """
    model = Vehicle
    form_class = VehicleForm

    def get_success_url(self):
        return reverse(
            "crm:vehicle-detail",
            kwargs={"pk": self.object.pk}
        )


class VehicleUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Vehicle update view, redirects to DetailView template
    """
    model = Vehicle
    form_class = VehicleUpdateForm

    def get_success_url(self):
        return reverse(
            "crm:vehicle-detail",
            kwargs={"pk": self.object.pk}
        )


class VehicleDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Vehicle delete view
    """
    model = Vehicle
    success_url = reverse_lazy("crm:vehicle-list")


class ClientListView(LoginRequiredMixin, generic.ListView):
    """
    Client list view, ordering by last order date
    Searching through the client last name
    """
    model = Client
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = ClientLastNameSearchForm(
            self.request.GET or None
        )
        return context

    def get_queryset(self):
        queryset = Client.objects.annotate(
             last_order_date=Max("orders__created_at")
         ).order_by("-last_order_date")
        form = ClientLastNameSearchForm(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data["q"]
            if q:
                queryset = queryset.filter(
                    last_name__icontains=q
                )

        return queryset.prefetch_related("orders", "vehicles")


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Client detail view
    """
    model = Client

    def get_queryset(self):
        return super().get_queryset().prefetch_related("orders", "vehicles")


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Client create view, redirects to DetailView template
    """
    form_class = ClientForm
    model = Client

    def get_success_url(self):
        return reverse(
            "crm:client-detail",
            kwargs={"pk": self.object.pk}
        )


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Client delete view
    """
    model = Client
    success_url = reverse_lazy("crm:client-list")


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Client update view, redirects to DetailView template
    """
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse(
            "crm:client-detail",
            kwargs={"pk": self.object.pk}
        )
