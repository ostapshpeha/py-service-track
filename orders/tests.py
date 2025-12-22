from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


User = get_user_model()


class InvoiceCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="manager", password="123")
        self.client.force_login(self.user)
        self.client_ob = Client.objects.create(
            first_name="John",
            last_name="Doe",
            mobile_number="+380000000010",
        )
        self.vehicle = Vehicle.objects.create(
            name="Test Vehicle",
            number_registration="BC1254AA",
            client=self.client_ob,
        )
        self.order = Order.objects.create(
            client=self.client_ob,
            vehicle=self.vehicle,
            requirements="Replace brakes",
        )
        self.url = reverse("orders:invoice-create", kwargs={"pk": self.order.pk})

    def test_get_initial_order(self):
        response = self.client.get(self.url, {"order": self.order.pk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.context["form"].initial["order"].pk), self.order.pk)

    def test_invoice_creation_redirect(self):
        form_data = {
            "order": self.order.pk,
            "parts_total": 1500.00,
        }

        response = self.client.post(self.url, data=form_data)


        self.assertEqual(Invoice.objects.count(), 1)
        new_invoice = Invoice.objects.first()

        expected_url = reverse("orders:order-detail", kwargs={"pk": new_invoice.pk})
        self.assertRedirects(response, expected_url)

    def test_create_invoice_without_order_get_param(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("order", response.context["form"].initial)
