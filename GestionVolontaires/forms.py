from django import forms
from .models import Volunteer

class VolunteerForm(forms.ModelForm):
    SPECIALITE_CHOICES = [
        ('medecin', 'Médecin'),
        ('infermier', 'Infirmier/ère'),
        ('psychologue', 'Psychologue'),
    ]

    specialite = forms.ChoiceField(
        choices=SPECIALITE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Spécialité',
    )

    class Meta:
        model = Volunteer
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'ville', 'adresse',
            'age', 'date_inscription', 'specialite', 'sexe', 'disponibilite', 'photo',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'date_inscription': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'disponibilite': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'prenom': 'Prénom',
            'telephone': 'Téléphone',
            'date_inscription': "Date d'inscription",
        }
        field_order = [
            'nom', 'prenom', 'email', 'telephone', 'ville', 'adresse',
            'age', 'date_inscription', 'specialite', 'sexe', 'disponibilite', 'photo',
        ]