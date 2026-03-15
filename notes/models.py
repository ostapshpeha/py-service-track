from cloudinary.models import CloudinaryField
from django.db import models

from accounts.models import CustomUser
from orders.models import Order


class Note(models.Model):
    """
    Note model it's mechanic's records about the car, with media add feature
    """

    description = models.TextField()
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="notes", null=True
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="notes"
    )
    date = models.DateTimeField(auto_now_add=True)
    picture = CloudinaryField("image", blank=True, null=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Note #{self.id} by {self.author} for {self.order}"
