from django.test import TestCase
from django.core.exceptions import ValidationError

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
