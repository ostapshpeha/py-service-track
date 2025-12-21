from django.db import models
from simple_history.models import HistoricalRecords


class Client(models.Model):
    """
    The customer model is related to vehicles one-to-many
    """
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    mobile_number = models.CharField(max_length=10, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"



class Vehicle(models.Model):
    """
    The vehicle model is related to only one client
    """
    class Engine(models.TextChoices):
        HYBRID = "hy", "Hybrid"
        ELECTRO = "el", "Electro"
        DIESEL = "di", "Diesel"
        PETROL = "pe", "Petrol"

    name = models.CharField(max_length=155)
    vin_code = models.CharField(max_length=17, unique=True)
    number_registration = models.CharField(max_length=10, unique=True)
    engine_type = models.CharField(max_length=2, choices=Engine.choices)
    last_service = models.DateField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name="vehicles", null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "vehicle"
        verbose_name_plural = "vehicles"
        ordering = ["last_service"]

    def __str__(self):
        return f"{self.name} ({self.number_registration})"
