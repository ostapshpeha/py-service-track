from django.test import TestCase

from django.urls import reverse
from django.contrib.auth import get_user_model


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