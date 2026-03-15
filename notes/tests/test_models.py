from django.test import TestCase
from django.contrib.auth import get_user_model

from crm.models import Client, Vehicle
from orders.models import Order
from notes.models import Note

User = get_user_model()


class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mechanic_1", password="password567"
        )
        self.client_obj = Client.objects.create(
            first_name="Taras", last_name="Sheva", mobile_number="0501112233"
        )
        self.vehicle = Vehicle.objects.create(
            name="Audi A6",
            vin_code="ABC12345678901234",
            number_registration="AA7777BB",
            engine_type=Vehicle.Engine.DIESEL,
            client=self.client_obj,
        )
        self.order = Order.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            requirements="Test requirements",
        )

    def test_note_creation(self):
        """
        Testing successful creation of a note
        """
        note = Note.objects.create(
            description="Oil change", order=self.order, author=self.user
        )
        self.assertEqual(Note.objects.count(), 1)
        self.assertIn("Note #", str(note))
        self.assertIn("mechanic_1", str(note))

    def test_cascade_delete_order(self):
        """
        Testing deletion of an Order, notes should be deleted too
        """
        Note.objects.create(
            description="Check engine", order=self.order, author=self.user
        )
        self.order.delete()
        self.assertEqual(Note.objects.count(), 0)

    def test_set_null_author_delete(self):
        """
        Testing deletion of a  mechanic , notes should be saved
        """
        note = Note.objects.create(
            description="Important", order=self.order, author=self.user
        )
        self.user.delete()

        note.refresh_from_db()
        self.assertIsNone(note.author)
        self.assertEqual(Note.objects.count(), 1)
