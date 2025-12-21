from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Max
from django.urls import reverse_lazy, reverse
from django.views import generic

from crm.forms import ClientForm, VehicleForm, VehicleUpdateForm, ClientLastNameSearchForm, VehicleNumberSearchForm
from crm.models import Vehicle, Client


class VehicleListView(LoginRequiredMixin, generic.ListView):
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

        return queryset


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

        return queryset


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
