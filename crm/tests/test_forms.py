from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from crm.forms import validate_vin_code


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