from django.db import models


class Field(models.Model):

    SOIL_TYPES = [
        ('CLAY', 'Clay'),
        ('SANDY', 'Sandy'),
        ('SILT', 'Silt'),
        ('LOAM', 'Loam'),
        ('BLACK', 'Black Soil'),
        ('RED', 'Red Soil'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)

    location = models.CharField(max_length=200, blank=True)

    area = models.DecimalField(max_digits=10, decimal_places=2)

    soil_type = models.CharField(
        max_length=20,
        choices=SOIL_TYPES,
        default='OTHER'
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name