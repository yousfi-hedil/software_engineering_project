from django.db import models
from django.utils import timezone

class Volunteer(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    specialite = models.CharField(max_length=120, blank=True)

    SEXE_CHOICES = (
        ('homme', 'Homme'),
        ('femme', 'Femme'),
    )
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES, blank=True)

    disponibilite = models.CharField(
        max_length=30,
        blank=True,
        choices=[
            ('matin', 'Matin'),
            ('apres_midi', 'Après-midi'),
            ('soir', 'Soir'),
            ('weekend', 'Week-end'),
            ('tous_les_jours', 'Tous les jours'),
        ],
    )
    photo = models.ImageField(upload_to='volunteers/', blank=True, null=True)
    date_inscription = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nom} {self.prenom}"
