
from django import forms
from django.utils import timezone

from .models import Harvest


class HarvestForm(forms.ModelForm):

    class Meta:
        model = Harvest

        fields = [
            'crop',
            'harvest_date',
            'quantity',
            'unit',
            'quality',
            'selling_price',
            'notes',
        ]

        widgets = {
            'crop': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),

            'harvest_date': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date',
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter harvested quantity',
                'step': '0.01',
                'min': '0.01',
            }),

            'unit': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. kg, tonnes, bags',
            }),

            'quality': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),

            'selling_price': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter selling price',
                'step': '0.01',
                'min': '0',
            }),

            'notes': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4,
                'placeholder': 'Additional harvest notes...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['harvest_date'].initial = (
            timezone.localdate()
        )

        self.fields['crop'].queryset = (
            self.fields['crop'].queryset.select_related(
                'category',
                'field',
            )
        )

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is not None and quantity <= 0:
            raise forms.ValidationError(
                'Harvest quantity must be greater than zero.'
            )

        return quantity

    def clean_selling_price(self):
        selling_price = self.cleaned_data.get('selling_price')

        if selling_price is not None and selling_price < 0:
            raise forms.ValidationError(
                'Selling price cannot be negative.'
            )

        return selling_price

    def clean_unit(self):
        unit = self.cleaned_data.get('unit')

        if unit:
            unit = unit.strip()

            if not unit:
                raise forms.ValidationError(
                    'Please enter a valid measurement unit.'
                )

        return unit
