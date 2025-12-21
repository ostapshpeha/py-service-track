from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model to inherit from AbstractUser
    This is our staff's accounts
    """
    class Role(models.TextChoices):
        MECHANIC = "mechanic", "Mechanic"
        MANAGER = "manager", "Manager"

    class MechanicPosition(models.TextChoices):
        AUTO_ELECTRICIAN = "AE", "Auto Electrician"
        ENGINE = "ENG", "Engine specialist"
        JUNIOR = "JUN", "Junior mechanic"
        ALIGNMENT = "ALI", "Wheel alignment specialist"
        TRANSMISSION = "TRS", "Transmission specialist"
        SENIOR = "SNR", "Senior mechanic"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MECHANIC)

    mechanic_position = models.CharField(
        max_length=32,
        choices=MechanicPosition.choices,
        blank=True,
        default="",
    )

    def clean(self):
        super().clean()
        if self.role != self.Role.MECHANIC and self.mechanic_position:
            raise ValidationError({"mechanic_position": "This position is only for mechanics"})
