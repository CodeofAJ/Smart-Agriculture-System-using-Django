
from django import forms
from .models import Inventory


class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory

        fields = [
            'name',
            'item_type',
            'quantity',
            'unit',
            'minimum_quantity',
            'unit_price',
            'description',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter item name',
            }),

            'item_type': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter available quantity',
                'step': '0.01',
                'min': '0',
            }),

            'unit': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. kg, litre, packet, pieces',
            }),

            'minimum_quantity': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter minimum stock level',
                'step': '0.01',
                'min': '0',
            }),

            'unit_price': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter price per unit',
                'step': '0.01',
                'min': '0',
            }),

            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4,
                'placeholder': 'Enter item description...',
            }),
        }

    # Validate item name
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name:
            name = name.strip()

            if not name:
                raise forms.ValidationError(
                    'Item name cannot be empty.'
                )

        return name

    # Validate quantity
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is not None and quantity < 0:
            raise forms.ValidationError(
                'Quantity cannot be negative.'
            )

        return quantity

    # Validate minimum quantity
    def clean_minimum_quantity(self):
        minimum_quantity = self.cleaned_data.get(
            'minimum_quantity'
        )

        if minimum_quantity is not None and minimum_quantity < 0:
            raise forms.ValidationError(
                'Minimum quantity cannot be negative.'
            )

        return minimum_quantity

    # Validate unit price
    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')

        if unit_price is not None and unit_price < 0:
            raise forms.ValidationError(
                'Unit price cannot be negative.'
            )

        return unit_price

    # Validate unit
    def clean_unit(self):
        unit = self.cleaned_data.get('unit')

        if unit:
            unit = unit.strip()

            if not unit:
                raise forms.ValidationError(
                    'Unit cannot be empty.'
                )

        return unit
