from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models.aggregates import Max
from django.shortcuts import render, redirect
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

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get("client_id")
        if client_id:
            try:
                client = Client.objects.get(pk=client_id)
                initial["client"] = client
            except Client.DoesNotExist:
                pass
        return initial

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


class ClientVehicleCreateView(LoginRequiredMixin, generic.View):
    """
    Simultaneous creation of Client and Vehicle.
    """
    template_name = "crm/client_vehicle_form.html"

    def get(self, request, *args, **kwargs):
        client_form = ClientForm(prefix="client")
        client_form.helper.form_tag = False
        vehicle_form = VehicleForm(prefix="vehicle")
        vehicle_form.helper.form_tag = False
        
        return render(request, self.template_name, {
            "client_form": client_form,
            "vehicle_form": vehicle_form,
        })

    def post(self, request, *args, **kwargs):
        client_form = ClientForm(request.POST, prefix="client")
        client_form.helper.form_tag = False
        vehicle_form = VehicleForm(request.POST, prefix="vehicle")
        vehicle_form.helper.form_tag = False

        if client_form.is_valid() and vehicle_form.is_valid():
            with transaction.atomic():
                client = client_form.save()
                vehicle = vehicle_form.save(commit=False)
                vehicle.client = client
                vehicle.save()
            return redirect("crm:vehicle-detail", pk=vehicle.pk)

        return render(request, self.template_name, {
            "client_form": client_form,
            "vehicle_form": vehicle_form,
        })
