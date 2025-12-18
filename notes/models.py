from django.db import models

from accounts.models import CustomUser
from crm.models import Vehicle


class Note(models.Model):
    description = models.TextField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="notes")
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="/notes", null=True, blank=True)

    def __str__(self):
        return f"Note #{self.id} by {self.author} for {self.vehicle}"