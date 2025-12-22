from django.db import models

from accounts.models import CustomUser
from crm.models import Vehicle


class Note(models.Model):
    """
    Note model it's mechanic's records about the car, with media add feature
    """
    description = models.TextField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="notes")
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="notes/pics/", null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Note #{self.id} by {self.author} for {self.vehicle}"