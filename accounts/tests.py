from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class CustomUserModelTest(TestCase):

    def test_create_valid_mechanic(self):
        """
        Test: Mechanic with a position should be valid.
        """
        user = CustomUser(
            username="mech_user",
            password="password123",
            role=CustomUser.Role.MECHANIC,
            mechanic_position=CustomUser.MechanicPosition.AUTO_ELECTRICIAN
        )
        try:
            user.full_clean()
            user.save()
        except ValidationError:
            self.fail("Valid mechanic raised ValidationError unexpectedly!")

        self.assertEqual(user.role, "mechanic")
        self.assertEqual(user.mechanic_position, "AE")

    def test_create_valid_manager(self):
        """
        Test: Manager without a mechanic_position should be valid.
        """
        user = CustomUser(
            username="manager_user",
            password="password123",
            role=CustomUser.Role.MANAGER,
            mechanic_position=""
        )
        try:
            user.full_clean()
            user.save()
        except ValidationError:
            self.fail("Valid manager raised ValidationError unexpectedly!")

        self.assertEqual(user.role, "manager")
        self.assertEqual(user.mechanic_position, "")

    def test_manager_cannot_have_mechanic_position(self):
        """
        Test: Manager WITH a mechanic_position should raise ValidationError.
        """
        user = CustomUser(
            username="bad_manager",
            password="password123",
            role=CustomUser.Role.MANAGER,
            mechanic_position=CustomUser.MechanicPosition.SENIOR
        )

        with self.assertRaises(ValidationError) as context:
            user.full_clean()

        self.assertIn("mechanic_position", context.exception.message_dict)
        self.assertEqual(
            context.exception.message_dict["mechanic_position"][0],
            "This position is only for mechanics"
        )


User = get_user_model()


class DashboardViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="staff", password="password123")
        self.client.force_login(self.user)
        self.url = reverse("accounts:index")

    def test_login_required(self):
        """Test that login is required to view the dashboard."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
