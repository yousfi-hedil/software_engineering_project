from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Sang(models.Model):
    id_sang = models.AutoField(primary_key=True)
    GROUPES_SANGUINS = [
        ("A", "A"),
        ("B", "B"),
        ("AB", "AB"),
        ("O", "O"),
    ]
    groupe_sanguin = models.CharField(max_length=2,choices=GROUPES_SANGUINS)
    RHESUS=[
        ("+","+"),
        ("-","-"),
    ]
    rhesus = models.CharField(max_length=1,choices=RHESUS)
    quantite = models.DecimalField(
        max_digits=4,        
        decimal_places=2,    
        default=0.00,
        help_text="Quantité de sang en litres (ex: 0.50)"
    )
    TYPE_DON = [
        ("Plasma", "Plasma"),
        ("Sang total", "Sang total"),
        ("Plaquettes", "Plaquettes"),
    ]
    type_don = models.CharField(max_length=30,choices=TYPE_DON)
    STATUS=[
        ("Disponible","Disponible"),
        ("Distribué","Distribué"),
        ("Réservé","Réservé"),
    ]
    status=models.CharField(max_length=50,choices=STATUS)
    date_collecte = models.DateField()
    date_expiration = models.DateField()
    lieu_stockage = models.CharField(max_length=100)
    def clean(self):
        if self.date_collecte and self.date_expiration:
            if self.date_expiration <= self.date_collecte:
                raise ValidationError("La date d'expiration doit être postérieure à la date de collecte.")

        dure_conservation = (self.date_expiration - self.date_collecte).days
        if dure_conservation > 42:
            raise ValidationError("La durée de conservation réelle du sang ne doit pas dépasser 42 jours après la date de collecte.")

        today = timezone.now().date()
        if self.date_collecte and self.date_collecte > today:
            raise ValidationError("La date de collecte ne peut pas être dans le futur.")
