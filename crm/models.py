from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    mobile_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"
        ordering = ["last_name", "first_name"]


class Vehicle(models.Model):
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

    def __str__(self):
        return f"{self.name} ({self.number_registration})"


# class CarPart(models.Model):
#     class Type(models.TextChoices):
#         ENGINE = "eng", "Engine"
#         TRANSMISSION = "trs", "Transmission"
#         BRAKES = "brk", "Brakes"
#         BODY = "bod", "Body"
#         ELECTRONICS = "elc", "Electronics"
#         UNDERCARRIAGE = "und", "Undercarriage"
#         OTHER = "other", "Other"
#
#     name = models.CharField(max_length=155)
#     price = models.DecimalField(decimal_places=2, max_digits=10)
#     type_of_part = models.CharField(max_length=10, choices=Type.choices)
