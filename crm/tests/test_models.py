from django.test import TestCase
from django.db.utils import IntegrityError
from crm.models import Client, Vehicle


class ClientModelTest(TestCase):
    def setUp(self):
        self.client_data = {
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "mobile_number": "0671234567",
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
                first_name="Petro", last_name="Sidorov", mobile_number="0671234567"
            )


class VehicleModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            first_name="Oleg", last_name="Petrov", mobile_number="0990001122"
        )
        self.vehicle_data = {
            "name": "Toyota Camry",
            "vin_code": "1234567890ABCDEFG",
            "number_registration": "AA1234BB",
            "engine_type": Vehicle.Engine.HYBRID,
            "client": self.client,
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
                engine_type=Vehicle.Engine.PETROL,
            )

    def test_on_delete_set_null(self):
        """
        Test that vehicle will not be deleted with client
        """
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        self.client.delete()

        vehicle.refresh_from_db()
        self.assertIsNone(vehicle.client)
