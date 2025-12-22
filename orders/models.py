from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from simple_history.models import HistoricalRecords

from crm.models import Client, Vehicle


class Order(models.Model):
    """
    Order model - core of the project,
    here described how service order should be looked
    Implemented History records feature to track who
    did CRUD operations with object
    """
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
        ordering = ["-created_at"]


class Invoice(models.Model):
    """
    Invoice model - an important addition to the order,
    it only shows the order amount,
    model collects simple data on how much the customer paid
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="invoice",
    )
    parts_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    history = HistoricalRecords()

    def work_total(self) -> Decimal:
        """
        Auto calculating price for work with coefficient 0.75 to parts price
        :return: Decimal value of work price
        """
        return (self.parts_total * Decimal("0.75")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total(self) -> Decimal:
        """
        Adding price for parts and work, it's the total price of invoice
        :return: Decimal value of total price
        """
        return (self.parts_total + self.work_total()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"Invoice for Order #{self.order_id} — Total for parts and work: {self.total}"