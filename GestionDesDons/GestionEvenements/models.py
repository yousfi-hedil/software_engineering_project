from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator,MinLengthValidator
from django.utils import timezone


titre_validateur = RegexValidator(
    regex=r'^[A-Za-z]+$',
    message="Ce champ ne doit contenir que des lettres"
)

class Evenement(models.Model):
    id_evenement = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100, validators=[titre_validateur])
    description = models.TextField(
        validators=[MinLengthValidator(30, message="La description doit contenir au moins 30 caractères.")]
    )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nb_participants = models.IntegerField()
    
    STATUT = [
        ("En cours", "En cours"),
        ("Terminé", "Terminé"),
        ("Prévu", "Prévu"),
    ]
    statut = models.CharField(max_length=50, choices=STATUT)
    lieu_evenement = models.CharField(max_length=200)
    image = models.ImageField(upload_to='evenements/', null=True, blank=True) 
    def clean(self):
        errors = {}

        if self.date_debut and self.date_fin:
            if self.date_debut > self.date_fin:
                errors['date_fin'] = "La date de fin doit être supérieure ou égale à la date de début."

        if self.date_debut:
            now = timezone.now()
            if self.date_debut < now:
                errors['date_debut'] = "Vous ne pouvez pas soumettre un événement déjà passé."

        if errors:
            raise ValidationError(errors)
