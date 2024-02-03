from django.db import models

from services.apps.pets.models import Pet


class Order(models.Model):
    petId = models.PositiveIntegerField(null=False, default=1)
    quantity = models.IntegerField()
    shipDate = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [('placed', 'Placed'), ('approved', 'Approved'), ('delivered', 'Delivered'), ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='placed')
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.pet.name} (Status: {self.status}, Complete: {self.complete})"
