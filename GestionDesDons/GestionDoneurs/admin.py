from django.contrib import admin
from django import forms
from .models import BloodDonation, RefusedDonation

# ==========================
# Formulaire personnalisé pour BloodDonation
# ==========================
class BloodDonationAdminForm(forms.ModelForm):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    ANTECEDENT_CHOICES = [
        ('operation', "une operation chirugicale"),
        ('tatouage_piercing', "un tatouage ou piercing"),
        ('infection_fievre', "une infection ou fiévre"),
        ('grossesse_accouchement', "une grossesse ou accouchement"),
        ('aucun', 'Aucun'),
    ]

    antecedents_recents = forms.MultipleChoiceField(
        choices=ANTECEDENT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Avez-vous eu récemment (moins de 6 mois) :",
    )

    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        required=True,
        widget=forms.Select,
        label='Groupe sanguin',
    )

    maladie_chronique = forms.TypedChoiceField(
        choices=[(True, 'Oui'), (False, 'Non')],
        coerce=lambda v: v == 'True' or v is True,
        widget=forms.RadioSelect,
        initial=False,
        required=True,
        label="Souffrez-vous actuellement d'une maladie chronique ?",
    )

    traitement_medical = forms.TypedChoiceField(
        choices=[(True, 'Oui'), (False, 'Non')],
        coerce=lambda v: v == 'True' or v is True,
        widget=forms.RadioSelect,
        initial=False,
        required=True,
        label='Prenez-vous un traitement médical ?'
    )

    class Meta:
        model = BloodDonation
        fields = [
            'nom', 'prenom', 'mail', 'telephone', 'adresse', 'poids', 'blood_group',
            'maladie_chronique', 'traitement_medical', 'antecedents_recents'
        ]

    def clean_antecedents_recents(self):
        values = self.cleaned_data.get('antecedents_recents', [])
        if 'aucun' in values:
            return []
        return values


# ==========================
# Admin BloodDonation
# ==========================
@admin.register(BloodDonation)
class BloodDonationAdmin(admin.ModelAdmin):
    form = BloodDonationAdminForm
    list_display = (
        'nom', 'prenom', 'blood_group', 'telephone', 'mail', 'poids',
        'maladie_chronique_display', 'traitement_medical_display', 'antecedents_display', 'created_at',
    )
    search_fields = (
        'nom', 'prenom', 'mail', 'telephone', 'blood_group',
    )
    list_filter = (
        'blood_group', 'maladie_chronique', 'traitement_medical', 'created_at',
    )
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def maladie_chronique_display(self, obj):
        return 'Oui' if obj.maladie_chronique else 'Non'
    maladie_chronique_display.short_description = "Maladie chronique"

    def traitement_medical_display(self, obj):
        return 'Oui' if obj.traitement_medical else 'Non'
    traitement_medical_display.short_description = "Traitement médical"

    def antecedents_display(self, obj):
        mapping = {
            'operation': "une operation chirugicale",
            'tatouage_piercing': "un tatouage ou piercing",
            'infection_fievre': "une infection ou fiévre",
            'grossesse_accouchement': "une grossesse ou accouchement",
        }
        values = obj.antecedents_recents or []
        if not values:
            return 'Aucun'
        labels = [mapping.get(v, v) for v in values]
        return ', '.join(labels)
    antecedents_display.short_description = "Antécédents récents"


# ==========================
# Admin RefusedDonation
# ==========================
@admin.register(RefusedDonation)
class RefusedDonationAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'prenom', 'blood_group', 'created_at',
    )
    search_fields = (
        'nom', 'prenom', 'mail', 'telephone', 'blood_group',
    )
    list_filter = (
        'blood_group', 'created_at',
    )
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
