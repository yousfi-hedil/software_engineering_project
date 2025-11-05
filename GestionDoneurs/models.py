from django.db import models

class BloodDonation(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mail = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    poids = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    blood_group = models.CharField(max_length=5)
    maladie_chronique = models.BooleanField(default=False)
    traitement_medical = models.BooleanField(default=False)
    antecedents_recents = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'donors'

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.blood_group}"


class RefusedDonation(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mail = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    reasons = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'refused_donations'

    def __str__(self):
        return f"Refus {self.nom} {self.prenom}"
