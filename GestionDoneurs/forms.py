from django import forms
from datetime import date
import re
from .models import BloodDonation

class BloodDonationForm(forms.ModelForm):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    YES_NO_CHOICES = [
        (False, 'Non'),
        (True, 'Oui'),
    ]

    # Extra (non-model) field: Date de naissance (obligatoire pour calcul âge)
    date_naissance = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
        label='Date de naissance',
    )

    # Override widgets/choices for model fields
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        label='Groupe sanguin',
        required=True,
    )
    traitement_medical = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda v: str(v).lower() in ('true', '1', 'oui', 'yes'),
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        label='Suivez-vous un traitement médical ?',
        required=True,
    )
    maladie_chronique = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda v: str(v).lower() in ('true', '1', 'oui', 'yes'),
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        label='Avez-vous une maladie chronique ?',
        required=True,
    )
    antecedents_recents = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('aucun', 'Aucun'),
            ('tatouage_piercing', 'Tatouage / Piercing'),
            ('grossesse_accouchement', 'Grossesse / Accouchement'),
        ],
        label='Antécédents récents',
    )

    class Meta:
        model = BloodDonation
        fields = [
            'nom', 'prenom', 'mail', 'telephone', 'adresse',
            'poids', 'blood_group', 'traitement_medical', 'maladie_chronique', 'antecedents_recents',
        ]
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'mail': 'Email',
            'telephone': 'Téléphone',
            'adresse': 'Adresse',
            'poids': 'Poids (kg)',
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'minlength': '2'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'minlength': '2'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'inputmode': 'numeric', 'pattern': '^\d{8}$', 'maxlength': '8'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'minlength': '5'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Forcer tous les champs comme obligatoires, même si le modèle a blank=True
        for name in ['nom', 'prenom', 'mail', 'telephone', 'adresse', 'poids', 'blood_group', 'traitement_medical', 'maladie_chronique', 'antecedents_recents']:
            if name in self.fields:
                self.fields[name].required = True
        # En édition, ne pas exiger la date de naissance (non stockée en BD)
        if 'date_naissance' in self.fields and getattr(self.instance, 'pk', None):
            self.fields['date_naissance'].required = False

    def _compute_age(self, d: date) -> int:
        today = date.today()
        return today.year - d.year - ((today.month, today.day) < (d.month, d.day))

    def clean(self):
        cleaned = super().clean()
        reasons = []
        is_create = not getattr(self.instance, 'pk', None)

        # Âge: refus si mineur (< 18 ans)
        dob = cleaned.get('date_naissance')
        if dob:
            age = self._compute_age(dob)
            if age < 18:
                reasons.append('Âge mineur (< 18 ans)')
        else:
            # En création on exige la date de naissance, en édition on ne l'impose pas
            if is_create:
                self.add_error('date_naissance', 'La date de naissance est requise')

        # Poids: > 50 kg requis (contrôle d'éligibilité en création uniquement)
        poids = cleaned.get('poids')
        if poids is not None:
            try:
                if float(poids) <= 50:
                    if is_create:
                        reasons.append('Poids insuffisant (doit être > 50 kg)')
            except (TypeError, ValueError):
                self.add_error('poids', 'Valeur de poids invalide')

        # Règles médicales: refus si Oui (création uniquement)
        if cleaned.get('maladie_chronique'):
            if is_create:
                reasons.append('Maladie chronique')
        if cleaned.get('traitement_medical'):
            if is_create:
                reasons.append('Traitement médical en cours')

        # Antécédents récents
        antecedents = cleaned.get('antecedents_recents') or []
        if not antecedents:
            self.add_error('antecedents_recents', 'Veuillez sélectionner une option')
        # "Aucun" exclusif
        if 'aucun' in antecedents and len(antecedents) > 1:
            self.add_error('antecedents_recents', "'Aucun' ne peut pas être sélectionné avec d'autres options")
        blocked = {
            'tatouage_piercing': "Tatouage/Piercing récent",
            'grossesse_accouchement': "Grossesse/Accouchement récent",
        }
        for key in antecedents:
            if key in blocked:
                if is_create:
                    reasons.append(blocked[key])

        # Invalidation avec raisons de refus: uniquement lors de la création
        if is_create and reasons:
            self.refusal_reasons = reasons
            from django.core.exceptions import ValidationError
            raise ValidationError(reasons)

        return cleaned

    # Champs obligatoires et formats
    def _validate_name(self, value: str, field_label: str) -> str:
        if value is None:
            raise forms.ValidationError(f"{field_label} est obligatoire")
        s = str(value).strip()
        if len(s) < 2:
            raise forms.ValidationError(f"{field_label} doit contenir au moins 2 caractères")
        # Lettres (y compris accentuées), espace, apostrophe et tiret
        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ' -]+", s):
            raise forms.ValidationError(f"{field_label} doit être une chaîne alphabétique valide")
        return s

    def clean_nom(self):
        return self._validate_name(self.cleaned_data.get('nom'), 'Nom')

    def clean_prenom(self):
        return self._validate_name(self.cleaned_data.get('prenom'), 'Prénom')

    def clean_adresse(self):
        v = self.cleaned_data.get('adresse')
        if v is None:
            raise forms.ValidationError("Adresse est obligatoire")
        s = str(v).strip()
        if len(s) < 5:
            raise forms.ValidationError("Adresse doit contenir au moins 5 caractères")
        # Doit contenir au moins une lettre ou un chiffre
        if not re.search(r"[\wÀ-ÖØ-öø-ÿ]", s):
            raise forms.ValidationError("Adresse invalide")
        return s

    def clean_telephone(self):
        v = self.cleaned_data.get('telephone')
        if v is None:
            raise forms.ValidationError("Téléphone est obligatoire")
        s = re.sub(r"\s+", "", str(v))
        if not re.fullmatch(r"\d{8}", s):
            raise forms.ValidationError("Téléphone doit contenir exactement 8 chiffres")
        return s