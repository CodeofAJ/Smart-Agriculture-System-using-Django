from django.db import models
from fields.models import Field


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Crop(models.Model):

    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('GROWING', 'Growing'),
        ('HARVESTED', 'Harvested'),
        ('FAILED', 'Failed'),
    ]

    name = models.CharField(max_length=150)

    variety = models.CharField(max_length=150, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='crops'
    )

    field = models.ForeignKey(
        Field,
        on_delete=models.PROTECT,
        related_name='crops'
    )

    planting_date = models.DateField()

    expected_harvest_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-planting_date']

    def __str__(self):
        return self.name