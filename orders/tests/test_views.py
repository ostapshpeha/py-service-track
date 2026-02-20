from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from crm.models import Client, Vehicle
from orders.models import Order, Invoice

User = get_user_model()


class InvoiceCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="manager", password="123")
        self.client.force_login(self.user)
        self.client_ob = Client.objects.create(
            first_name="John",
            last_name="Doe",
            mobile_number="0990000010",
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
        self.assertEqual(
            int(response.context["form"].initial["order"].pk), self.order.pk
        )

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
