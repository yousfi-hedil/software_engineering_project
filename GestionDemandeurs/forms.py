from django import forms
from .models import Demandeur
from django.contrib.auth.hashers import make_password

class DemandeurForm(forms.ModelForm):
    mdp = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'}),
        label='Mot de passe',
        required=True
    )

    confirm_mdp = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'}),
        label='Confirmer le mot de passe',
        required=True
    )

    class Meta:
        model = Demandeur
        fields = [
            'nom_user', 'prenom_user', 'cin_user', 'email_user',
            'mdp', 'confirm_mdp', 'sexe_user', 'DateNaissance',
            'telephone_user', 'adresse', 'institution', 'justificatifs'
        ]
        widgets = {
            'nom_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom'}),
            'prenom_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre prénom'}),
            'cin_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678', 'maxlength': '8'}),
            'email_user': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@email.com'}),
            'sexe_user': forms.Select(attrs={'class': 'form-select'}),
            'DateNaissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telephone_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678', 'maxlength': '8'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre adresse'}),
            'institution': forms.Select(attrs={'class': 'form-select'}),
            'justificatifs': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.png,.jpeg,.jpg'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mdp = cleaned_data.get('mdp')
        confirm_mdp = cleaned_data.get('confirm_mdp')

        if mdp and confirm_mdp and mdp != confirm_mdp:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        demandeur = super().save(commit=False)
        demandeur.mdp = make_password(self.cleaned_data['mdp'])
        if commit:
            demandeur.save()
        return demandeur
