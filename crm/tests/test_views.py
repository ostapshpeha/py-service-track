from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from crm.models import Client, Vehicle

User = get_user_model()


class SearchViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teststaff", password="password")
        self.client.force_login(self.user)

        self.c1 = Client.objects.create(
            first_name="Ivan", last_name="Bondarenko", mobile_number="0671112233"
        )
        self.c2 = Client.objects.create(
            first_name="Petro", last_name="Shevchenko", mobile_number="0674445566"
        )

        self.v1 = Vehicle.objects.create(
            name="BMW X5",
            vin_code="VIN11111111111111",
            number_registration="AA0001BB",
            engine_type=Vehicle.Engine.DIESEL,
        )
        self.v2 = Vehicle.objects.create(
            name="Tesla Model 3",
            vin_code="VIN22222222222222",
            number_registration="BC7777CB",
            engine_type=Vehicle.Engine.ELECTRO,
        )

    # ---  ClientListView ---

    def test_client_search_success(self):
        url = reverse("crm:client-list")
        response = self.client.get(url, {"q": "bondar"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bondarenko")
        self.assertNotContains(response, "Shevchenko")
        self.assertEqual(len(response.context["object_list"]), 1)

    def test_client_search_empty_results(self):
        url = reverse("crm:client-list")
        response = self.client.get(url, {"q": "UnknownName"})

        self.assertEqual(len(response.context["object_list"]), 0)

    # ---  VehicleListView ---

    def test_vehicle_search_by_number(self):
        url = reverse("crm:vehicle-list")
        response = self.client.get(url, {"q": "aa0001"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AA0001BB")
        self.assertNotContains(response, "BC7777CB")
        self.assertEqual(len(response.context["object_list"]), 1)

    def test_vehicle_list_without_search(self):
        url = reverse("crm:vehicle-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 2)
