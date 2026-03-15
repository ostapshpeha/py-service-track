from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from simple_history.models import HistoricalRecords

from accounts.models import CustomUser
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
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="assigned_orders",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    requirements = models.TextField()
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )
    mileage = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Vehicle mileage at the time of service",
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"Order #{self.pk} — {self.vehicle}"

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
        ordering = ["-created_at"]


class Part(models.Model):
    """
    Car-Parts Table for Inventory Management
    """

    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    name = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_level = models.IntegerField(default=0)
    category = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.sku} - {self.name}"

    class Meta:
        verbose_name = "part"
        verbose_name_plural = "parts"
        ordering = ["name"]


class OrderItem(models.Model):
    """
    Links parts to specific orders and tracks quantity/price
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Retail price at the time of order"
    )
    history = HistoricalRecords()

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.part.name} for Order #{self.order.pk}"

    class Meta:
        verbose_name = "order item"
        verbose_name_plural = "order items"


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
    parts_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Total cost of parts. Should match sum of Order Items.",
    )
    labor_hours = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal("0.00")
    )
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("50.00")
    )
    history = HistoricalRecords()

    def work_total(self) -> Decimal:
        """
        Auto calculating price for work based on labor hours and rate
        :return: Decimal value of work price
        """
        return (self.labor_hours * self.hourly_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def total(self) -> Decimal:
        """
        Adding price for parts and work, it's the total price of invoice
        :return: Decimal value of total price
        """
        return (self.parts_total + self.work_total()).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def __str__(self):
        return (
            f"Invoice for Order #{self.order_id} "
            f"— Total for parts and work: {self.total}"
        )
