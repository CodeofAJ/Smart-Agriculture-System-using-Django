from django.db import models
from crops.models import Crop


class Harvest(models.Model):

    QUALITY_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('AVERAGE', 'Average'),
        ('POOR', 'Poor'),
    ]

    crop = models.ForeignKey(
        Crop,
        on_delete=models.PROTECT,
        related_name='harvests'
    )

    harvest_date = models.DateField()

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    unit = models.CharField(max_length=30, default='kg')

    quality = models.CharField(
        max_length=20,
        choices=QUALITY_CHOICES,
        default='GOOD'
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop.name} - {self.harvest_date}"
    

class Expense(models.Model):

    EXPENSE_TYPES = [
        ('SEEDS', 'Seeds'),
        ('FERTILIZER', 'Fertilizer'),
        ('LABOUR', 'Labour'),
        ('EQUIPMENT', 'Equipment'),
        ('IRRIGATION', 'Irrigation'),
        ('TRANSPORT', 'Transport'),
        ('OTHER', 'Other'),
    ]

    crop = models.ForeignKey(
        Crop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )

    expense_type = models.CharField(
        max_length=20,
        choices=EXPENSE_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    expense_date = models.DateField()

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_expense_type_display()} - ₹{self.amount}"
