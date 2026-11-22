
from django import forms
from .models import Field


class FieldForm(forms.ModelForm):

    class Meta:
        model = Field

        fields = [
            'name',
            'location',
            'area',
            'soil_type',
            'description',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter field name',
            }),

            'location': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter field location',
            }),

            'area': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter area in acres',
                'step': '0.01',
                'min': '0.01',
            }),

            'soil_type': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),

            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4,
                'placeholder': 'Enter field description',
            }),
        }

    def clean_area(self):
        area = self.cleaned_data.get('area')

        if area is not None and area <= 0:
            raise forms.ValidationError(
                'Field area must be greater than zero.'
            )

        return area
