from django import forms
from .models import Crop


class CropForm(forms.ModelForm):

    class Meta:
        model = Crop

        fields = [
            'name',
            'variety',
            'category',
            'field',
            'planting_date',
            'expected_harvest_date',
            'status',
            'description',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crop name'
            }),

            'variety': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crop variety'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'field': forms.Select(attrs={
                'class': 'form-select'
            }),

            'planting_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'expected_harvest_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter crop description'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        planting_date = cleaned_data.get('planting_date')
        harvest_date = cleaned_data.get('expected_harvest_date')

        if planting_date and harvest_date:
            if harvest_date < planting_date:
                self.add_error(
                    'expected_harvest_date',
                    'Expected harvest date cannot be earlier than planting date.'
                )

        return cleaned_data