from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from crm.models import Client, Vehicle
from notes.models import Note


User = get_user_model()


class NoteListViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="mech1", first_name="Taras", last_name="Petrenko", password="123"
        )
        self.user2 = User.objects.create_user(
            username="mech2", first_name="Ivan", last_name="Mazepa", password="123"
        )
        self.client_obj = Client.objects.create(
            first_name="Taras",
            last_name="Sheva",
            mobile_number="0501112233"
        )
        self.vehicle = Vehicle.objects.create(
            name="Audi A6",
            vin_code="ABC12345678901234",
            number_registration="AA7777BB",
            engine_type=Vehicle.Engine.DIESEL,
            client=self.client_obj
        )

        Note.objects.create(description="Note 1", author=self.user1, vehicle=self.vehicle)
        Note.objects.create(description="Note 2", author=self.user2, vehicle=self.vehicle)

        self.client.force_login(self.user1)
        self.url = reverse("notes:note-list")

    def test_search_by_first_name(self):
        """
        Searching for name (Ivan)
        """
        response = self.client.get(self.url, {"q": "Ivan"})
        self.assertEqual(len(response.context["notes"]), 1)
        self.assertEqual(response.context["notes"][0].author.first_name, "Ivan")

    def test_search_by_last_name(self):
        """
        Searching for last name (Petrenko)
        """
        response = self.client.get(self.url, {"q": "petren"})
        self.assertEqual(len(response.context["notes"]), 1)
        self.assertEqual(response.context["notes"][0].author.last_name, "Petrenko")
