from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Max
from django.urls import reverse_lazy, reverse
from django.views import generic

from crm.forms import ClientForm, VehicleForm, VehicleUpdateForm
from crm.models import Vehicle, Client


class VehicleListView(LoginRequiredMixin, generic.ListView):
    model = Vehicle
    paginate_by = 30

    def get_queryset(self):
        return Vehicle.objects.all().order_by("-last_service")


class VehicleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Vehicle

    def get_queryset(self):
        return super().get_queryset().select_related("client")


class VehicleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Vehicle
    form_class = VehicleForm
    def get_success_url(self):
        return reverse(
            "crm:vehicle-detail",
            kwargs={"pk": self.object.pk}
        )


class VehicleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Vehicle
    form_class = VehicleUpdateForm
    def get_success_url(self):
        return reverse(
            "crm:vehicle-detail",
            kwargs={"pk": self.object.pk}
        )


class VehicleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Vehicle
    success_url = reverse_lazy("crm:vehicle-list")


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    paginate_by = 30

    def get_queryset(self):
        return Client.objects.annotate(
            last_order_date=Max("orders__created_at")
        ).order_by("-last_order_date")


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client

    def get_queryset(self):
        return super().get_queryset().prefetch_related("vehicles")


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ClientForm
    model = Client
    def get_success_url(self):
        return reverse(
            "crm:client-detail",
            kwargs={"pk": self.object.pk}
        )


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy("crm:client-list")


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientForm
    def get_success_url(self):
        return reverse(
            "crm:client-detail",
            kwargs={"pk": self.object.pk}
        )
