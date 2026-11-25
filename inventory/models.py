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
    

class InventoryTransaction(models.Model):

    TRANSACTION_TYPES = [
        ('STOCK_IN', 'Stock In'),
        ('STOCK_OUT', 'Stock Out'),
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.PROTECT,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    previous_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    new_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_date = models.DateField()

    reference = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        verbose_name = 'Inventory Transaction'
        verbose_name_plural = 'Inventory Transactions'

    def __str__(self):
        return (
            f"{self.get_transaction_type_display()} - "
            f"{self.inventory.name} - {self.quantity}"
        )

