from django.db import models
from crops.models import Crop


class FarmActivity(models.Model):

    ACTIVITY_TYPES = [
        ('IRRIGATION', 'Irrigation'),
        ('FERTILIZER', 'Fertilizer Application'),
        ('PESTICIDE', 'Pesticide Application'),
        ('WEEDING', 'Weeding'),
        ('PLOUGHING', 'Ploughing'),
        ('OTHER', 'Other'),
    ]

    crop = models.ForeignKey(
        Crop,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    activity_type = models.CharField(
        max_length=30,
        choices=ACTIVITY_TYPES
    )

    activity_date = models.DateField()

    description = models.TextField(blank=True)

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.crop.name}"