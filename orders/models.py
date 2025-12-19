from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from simple_history.models import HistoricalRecords

from crm.models import Client, Vehicle


class Order(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"
        NEEDS_CLARIFICATION = "needs_clarification", "Needs clarification"

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    requirements = models.TextField()
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"Order #{self.pk} — {self.vehicle}"

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
        ordering = ["invoice"]


class Invoice(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="invoice",
    )
    parts_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    history = HistoricalRecords()

    def work_total(self) -> Decimal:
        return (self.parts_total * Decimal("0.75")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total(self) -> Decimal:
        return (self.parts_total + self.work_total()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"Invoice for Order #{self.order_id} — Total: {self.total}"