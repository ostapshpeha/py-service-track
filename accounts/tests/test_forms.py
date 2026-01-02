from django.test import TestCase
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


class CustomUserCreationFormTests(TestCase):

    def setUp(self):
        self.base_data = {
            "username": "test_employee",
            "first_name": "Ivan",
            "last_name": "Tester",
            "email": "ivan@service.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

    def test_mechanic_creation_success(self):
        form_data = self.base_data.copy()
        form_data.update({
            "role": CustomUser.Role.MECHANIC,
            "mechanic_position": CustomUser.MechanicPosition.ENGINE
        })

        form = CustomUserCreationForm(data=form_data)

        if not form.is_valid():
            print(f"\nFORM ERRORS: {form.errors.as_json()}")

        self.assertTrue(form.is_valid())

    def test_mechanic_missing_position_error(self):
        form_data = self.base_data.copy()
        form_data.update({
            "role": CustomUser.Role.MECHANIC,
            "mechanic_position": ""
        })

        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("mechanic_position", form.errors)
        self.assertEqual(
            form.errors["mechanic_position"][0],
            "You must specify mechanic position"
        )

    def test_manager_auto_clears_position(self):
        form_data = self.base_data.copy()
        form_data.update({
            "role": CustomUser.Role.MANAGER,
            "mechanic_position": CustomUser.MechanicPosition.AUTO_ELECTRICIAN
        })

        form = CustomUserCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["mechanic_position"], "")

        user = form.save()
        self.assertEqual(user.role, CustomUser.Role.MANAGER)
        self.assertEqual(user.mechanic_position, "")

    def test_manager_creation_normal(self):
        form_data = self.base_data.copy()
        form_data.update({
            "role": CustomUser.Role.MANAGER,
            "mechanic_position": ""
        })

        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
