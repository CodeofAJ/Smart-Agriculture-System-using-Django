from django.db import models


class Inventory(models.Model):

    ITEM_TYPES = [
        ('SEEDS', 'Seeds'),
        ('FERTILIZER', 'Fertilizer'),
        ('PESTICIDE', 'Pesticide'),
        ('TOOLS', 'Tools'),
        ('EQUIPMENT', 'Equipment'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=150)

    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPES
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    unit = models.CharField(max_length=30)

    minimum_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_quantity