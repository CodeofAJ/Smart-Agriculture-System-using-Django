
from django import forms
from .models import FarmActivity


class FarmActivityForm(forms.ModelForm):
    class Meta:
        model = FarmActivity
        fields = [
            'crop',
            'activity_type',
            'activity_date',
            'description',
            'cost',
        ]

        widgets = {
            'crop': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),
            'activity_type': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),
            'activity_date': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4,
                'placeholder': 'Describe the farming activity...',
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter activity cost',
            }),
        }

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')

        if cost is not None and cost < 0:
            raise forms.ValidationError(
                'Activity cost cannot be negative.'
            )

        return cost
