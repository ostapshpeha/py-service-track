from decimal import Decimal

from django.test import TestCase

from crm.models import Client, Vehicle
from orders.models import Order, Invoice


class OrderModelTest(TestCase):

    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="John",
            last_name="Doe",
            mobile_number="+380000000000",
        )
        self.vehicle = Vehicle.objects.create(
            name="Test Vehicle",
            number_registration="BC1234AA",
            client=self.client_obj,
        )
        self.order = Order.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            requirements="Replace brakes",
        )

    def test_order_creation(self):
        order1 = self.order

        self.assertIsNotNone(order1.pk)
        self.assertEqual(order1.status, Order.Status.IN_PROGRESS)

    def test_invoice_creation(self):
        invoice = Invoice.objects.create(
            order=self.order,
            parts_total=Decimal("100.00"),
        )

        self.assertIsNotNone(invoice.pk)
        self.assertEqual(invoice.order, self.order)

    def test_work_total_calculation(self):
        invoice = Invoice.objects.create(
            order=self.order,
            parts_total=Decimal("100.00"),
        )

        self.assertEqual(
            invoice.work_total(),
            Decimal("75.00"),
        )

    def test_total_property(self):
        invoice = Invoice.objects.create(
            order=self.order,
            parts_total=Decimal("100.00"),
        )

        self.assertEqual(
            invoice.total,
            Decimal("175.00"),
        )
