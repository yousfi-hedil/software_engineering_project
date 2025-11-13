from django import forms
from datetime import date
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import BloodDonation, RefusedDonation

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

    date_naissance = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date de naissance',
    )

    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Groupe sanguin',
        required=True,
    )

    traitement_medical = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda v: str(v).lower() in ('true', '1', 'oui', 'yes'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Suivez-vous un traitement médical ?',
        required=True,
    )

    maladie_chronique = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda v: str(v).lower() in ('true', '1', 'oui', 'yes'),
        widget=forms.Select(attrs={'class': 'form-select'}),
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
            'ville', 'date_naissance', 'date_inscription',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '8'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'date_inscription': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force required on main fields for creation
        required_fields = [
            'nom', 'prenom', 'mail', 'telephone', 'adresse', 'poids', 'ville',
            'date_naissance', 'date_inscription', 'blood_group', 'traitement_medical',
            'maladie_chronique', 'antecedents_recents'
        ]
        for f in required_fields:
            if f in self.fields:
                self.fields[f].required = True

        # When editing existing instance, keep date_naissance optional
        if getattr(self.instance, 'pk', None):
            if 'date_naissance' in self.fields:
                self.fields['date_naissance'].required = False

    def _compute_age(self, d: date) -> int:
        today = date.today()
        return today.year - d.year - ((today.month, today.day) < (d.month, d.day))

    # Validation noms, adresse, téléphone
    def clean_nom(self):
        return self._validate_name(self.cleaned_data.get('nom'), 'Nom')

    def clean_prenom(self):
        return self._validate_name(self.cleaned_data.get('prenom'), 'Prénom')

    def clean_adresse(self):
        v = self.cleaned_data.get('adresse')
        if not v or len(v.strip()) < 5:
            raise forms.ValidationError("Adresse invalide (au moins 5 caractères)")
        return v.strip()

    def clean_ville(self):
        return self._validate_name(self.cleaned_data.get('ville'), 'Ville')

    def clean_mail(self):
        v = (self.cleaned_data.get('mail') or '').strip()
        if not v:
            raise forms.ValidationError('Email requis')
        try:
            validate_email(v)
        except DjangoValidationError:
            raise forms.ValidationError('Email invalide')
        return v

    def clean_telephone(self):
        v = re.sub(r"\s+", "", str(self.cleaned_data.get('telephone') or ''))
        if not re.fullmatch(r"\d{8}", v):
            raise forms.ValidationError("Téléphone doit contenir exactement 8 chiffres")
        return v

    def _validate_name(self, value: str, field_label: str) -> str:
        if not value or len(value.strip()) < 2:
            raise forms.ValidationError(f"{field_label} doit contenir au moins 2 caractères")
        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ' -]+", value.strip()):
            raise forms.ValidationError(f"{field_label} invalide")
        return value.strip()

    def clean_poids(self):
        v = self.cleaned_data.get('poids')
        if v in (None, ''):
            raise forms.ValidationError('Poids requis')
        try:
            val = float(v)
        except (TypeError, ValueError):
            raise forms.ValidationError('Poids invalide')
        if val <= 0:
            raise forms.ValidationError('Le poids doit être positif')
        return v

    def clean(self):
        cleaned = super().clean()
        dob = cleaned.get('date_naissance')
        if dob:
            cleaned['age'] = self._compute_age(dob)

        # Gestion des antécédents
        antecedents = cleaned.get('antecedents_recents') or []
        # normalize single-selection to list (POST may provide a single string)
        if isinstance(antecedents, str):
            antecedents = [antecedents]
        if not antecedents:
            self.add_error('antecedents_recents', 'Veuillez sélectionner au moins une option')
        if 'aucun' in antecedents and len(antecedents) > 1:
            antecedents = ['aucun']
            cleaned['antecedents_recents'] = antecedents

        # Stocker les raisons de refus sans bloquer la sauvegarde
        reasons = []
        if dob and cleaned.get('age', 0) < 18:
            reasons.append('Âge mineur (<18 ans)')
        poids = cleaned.get('poids')
        if poids is not None and float(poids) < 50:
            reasons.append('Poids insuffisant (<50 kg)')
        if cleaned.get('maladie_chronique'):
            reasons.append('Maladie chronique')
        if cleaned.get('traitement_medical'):
            reasons.append('Traitement médical en cours')
        # Antécédents spécifiques entraînant un refus
        if 'tatouage_piercing' in antecedents:
            reasons.append('Tatouage / Piercing')
        if 'grossesse_accouchement' in antecedents:
            reasons.append('Grossesse / Accouchement')

        self.refusal_reasons = reasons
        return cleaned

    def save(self, commit=True):
        # If there are refusal reasons, record the refusal and do not save a BloodDonation
        reasons = getattr(self, 'refusal_reasons', []) or []
        if reasons:
            # create a RefusedDonation record
            data = {
                'nom': self.cleaned_data.get('nom') or '',
                'prenom': self.cleaned_data.get('prenom') or '',
                'mail': self.cleaned_data.get('mail') or '',
                'telephone': self.cleaned_data.get('telephone') or '',
                'adresse': self.cleaned_data.get('adresse') or '',
                'blood_group': self.cleaned_data.get('blood_group') or '',
                'date_naissance': self.cleaned_data.get('date_naissance'),
                'poids': self.cleaned_data.get('poids'),
                'reasons': reasons,
            }
            refused = RefusedDonation.objects.create(**data)
            return refused

        # Otherwise save the normal BloodDonation
        instance = super().save(commit=False)
        dob = self.cleaned_data.get('date_naissance')
        if dob:
            instance.age = self._compute_age(dob) if hasattr(instance, 'age') else None
            instance.date_naissance = dob
        if commit:
            instance.save()
            self.save_m2m()
        return instance
