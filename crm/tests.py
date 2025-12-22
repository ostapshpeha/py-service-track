from django.core.exceptions import ValidationError
from django.test import TestCase, SimpleTestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import validate_vin_code
from .models import Client, Vehicle


class ClientModelTest(TestCase):
    def setUp(self):
        self.client_data = {
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "mobile_number": "0671234567"
        }

    def test_create_valid_client(self):
        client = Client.objects.create(**self.client_data)
        self.assertEqual(str(client), "Ivan Ivanov")
        self.assertEqual(Client.objects.count(), 1)

    def test_duplicate_mobile_number(self):
        """
        Duplicate mobile number must be rejected.
        """
        Client.objects.create(**self.client_data)
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                first_name="Petro",
                last_name="Sidorov",
                mobile_number="0671234567"
            )


class VehicleModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            first_name="Oleg",
            last_name="Petrov",
            mobile_number="0990001122"
        )
        self.vehicle_data = {
            "name": "Toyota Camry",
            "vin_code": "1234567890ABCDEFG",
            "number_registration": "AA1234BB",
            "engine_type": Vehicle.Engine.HYBRID,
            "client": self.client
        }

    def test_create_valid_vehicle(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        self.assertEqual(str(vehicle), "Toyota Camry (AA1234BB)")
        self.assertEqual(vehicle.client.first_name, "Oleg")

    def test_unique_vin_code(self):
        Vehicle.objects.create(**self.vehicle_data)
        with self.assertRaises(IntegrityError):
            Vehicle.objects.create(
                name="Honda Civic",
                vin_code="1234567890ABCDEFG",
                number_registration="BC9999AI",
                engine_type=Vehicle.Engine.PETROL
            )


    def test_on_delete_set_null(self):
        """
        Test that vehicle will not be deleted with client
        """
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        self.client.delete()

        vehicle.refresh_from_db()
        self.assertIsNone(vehicle.client)


User = get_user_model()


class SearchViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teststaff", password="password")
        self.client.force_login(self.user)

        self.c1 = Client.objects.create(first_name="Ivan", last_name="Bondarenko", mobile_number="0671112233")
        self.c2 = Client.objects.create(first_name="Petro", last_name="Shevchenko", mobile_number="0674445566")

        self.v1 = Vehicle.objects.create(
            name="BMW X5",
            vin_code="VIN11111111111111",
            number_registration="AA0001BB",
            engine_type=Vehicle.Engine.DIESEL
        )
        self.v2 = Vehicle.objects.create(
            name="Tesla Model 3",
            vin_code="VIN22222222222222",
            number_registration="BC7777CB",
            engine_type=Vehicle.Engine.ELECTRO
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


class VinValidatorTest(SimpleTestCase):

    def test_valid_vin(self):
        """
        Testing valid vin code
        """
        valid_vin = "1234567890ABCDEFG"
        try:
            result = validate_vin_code(valid_vin)
            self.assertEqual(result, valid_vin)
        except ValidationError:
            self.fail("validate_vin_code raised ValidationError unexpectedly!")

    def test_vin_too_short(self):
        """
        Testing invalid vin code
        """
        with self.assertRaises(ValidationError) as cm:
            validate_vin_code("gh123hg5hj5g5hhhh")
        self.assertEqual(
            cm.exception.message,
            "VIN should have big letters A-Z and numbers (0-9), without spaces"
        )
