from django import forms
from .models import Sang

class SangForm(forms.ModelForm):
    class Meta:
        model = Sang
        fields = [
            "groupe_sanguin", "rhesus", "type_don",
            "quantite", "status", "date_collecte", "date_expiration", "lieu_stockage"
        ]
        widgets = {
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'rhesus': forms.Select(attrs={'class': 'form-select'}),
            'type_don': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01, 'min': 0}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date_collecte': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_expiration': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lieu_stockage': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
    