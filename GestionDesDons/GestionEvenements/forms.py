from django import forms
from .models import Evenement

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = [
            "titre", "description", "date_debut", "date_fin",
            "nb_participants", "statut", "lieu_evenement", "image"
        ]
        widgets = {
            'date_debut': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'date_fin': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,       # hauteur du textarea
                    'style': 'resize: vertical; overflow-wrap: break-word;'
                }
            ),
            'nb_participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'lieu_evenement': forms.TextInput(attrs={'class': 'form-control'}),
        }
