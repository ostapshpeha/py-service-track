from django.urls import  path

from .views import (
    VehicleListView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientDeleteView,
    ClientUpdateView,
    index
)

app_name = "crm"

urlpatterns = [
    path("", index, name="index"),
    path("vehicles/", VehicleListView.as_view(), name="vehicle-list"),
    path("vehicles/<int:pk>/", VehicleDetailView.as_view(), name="vehicle-detail"),
    path("vehicles/create/", VehicleCreateView.as_view(), name="vehicle-create"),
    path("vehicles/<int:pk>/update/", VehicleUpdateView.as_view(), name="vehicle-update"),
    path("vehicles/<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle-delete"),
    path("clients/", ClientListView.as_view(), name="client-list"),
    path(
        "clients/<int:pk>/", ClientDetailView.as_view(), name="client-detail"
    ),
    path("clients/create/", ClientCreateView.as_view(), name="client-create"),
    path(
        "clients/<int:pk>/delete/",
        ClientDeleteView.as_view(),
        name="client-delete"
    ),
    path(
        "clients/<int:pk>/update/",
        ClientUpdateView.as_view(),
        name="client-update"
    ),
]
