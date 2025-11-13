from django.db import models
from django.core.validators import RegexValidator

class Demandeur(models.Model):
    SEXE_CHOICES = [
        ('Masculin', 'Masculin'),
        ('Féminin', 'Féminin'),
    ]
    
    INSTITUTION_CHOICES = [
        ('DonVia Tunis Nord (El Menzah)', 'DonVia Tunis Nord (El Menzah)'),
        ('DonVia Tunis Centre Bab Bhar', 'DonVia Tunis Centre Bab Bhar)'),
        ('DonVia Tunis Sud Ibn Khaldoun', 'DonVia Tunis Sud Ibn Khaldoun'),
        ('DonVia Ariana Ville', 'DonVia Ariana Ville'),
        ('DonVia Ben Arous Centre', 'DonVia Ben Arous Centre'),
        ('DonVia Manouba Douar Hicher', 'DonVia Manouba Douar Hicher'),
        ('DonVia Nabeul Ville', 'DonVia Nabeul Ville'),
        ('DonVia Sousse Riadh', 'DonVia Sousse Riadh'),
        ('DonVia Sfax Ville', 'DonVia Sfax Ville'),
        ('DonVia Kairouan Médina', 'DonVia Kairouan Médina'),
        ('DonVia Bizerte Ville', 'DonVia Bizerte Ville'),
        ('DonVia Gabès Ville', 'DonVia Gabès Ville'),
        ('DonVia Mimédenine Ville', 'DonVia Médenine Ville'),
        ('DonVia Tataouine Ville', 'DonVia Tataouine Ville'),
        ('DonVia Tozeur Centre', 'DonVia Tozeur Centre'),
        ('DonVia Gafsa Ville', 'DonVia Gafsa Ville'),
        ('DonVia Sidi Bouzid Ville', 'DonVia Sidi Bouzid Ville'),
        ('DonVia Kasserine Ville', 'DonVia Kasserine Ville'),
        ('DonVia Siliana Ville', 'DonVia Siliana Ville'),
        ('DonVia Béja Nord', 'DonVia Béja Nord'),
        ('DonVia Jendouba Ville', 'DonVia Jendouba Ville'),
        ('DonVia Le Kef Ville', 'DonVia Le Kef Ville'),
        ('DonVia Mahdia Ville', 'DonVia Mahdia Ville'),
        ('DonVia Zaghouan Ville', 'DonVia Zaghouan Ville'),
        ('DonVia Monastir Ville', 'DonVia Monastir Ville'),
    ]
    
    cin_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="Le CIN doit contenir exactement 8 chiffres."
    )
    
    telephone_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="Le numéro de téléphone doit contenir exactement 8 chiffres."
    )
    
    nom_user = models.CharField(max_length=100, verbose_name="Nom")
    prenom_user = models.CharField(max_length=100, verbose_name="Prénom")
    cin_user = models.CharField(
        max_length=8, 
        unique=True, 
        validators=[cin_validator],
        verbose_name="CIN"
    )
    email_user = models.EmailField(unique=True, verbose_name="Email")
    mdp = models.CharField(max_length=255, verbose_name="Mot de passe")
    sexe_user = models.CharField(max_length=10, choices=SEXE_CHOICES, verbose_name="Sexe")
    DateNaissance = models.DateField(verbose_name="Date de naissance")
    telephone_user = models.CharField(
        max_length=8,
        validators=[telephone_validator],
        verbose_name="Téléphone"
    )
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    institution = models.CharField(
        max_length=100,
        choices=INSTITUTION_CHOICES,
        verbose_name="Institution"
    )
    justificatifs = models.FileField(
        upload_to='demandeurs/justificatifs/',
        verbose_name="Documents justificatifs"
    )
    date_inscription_user = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    role = models.CharField(max_length=50, default='Demandeur', verbose_name="Rôle")
    
    class Meta:
        verbose_name = "Demandeur"
        verbose_name_plural = "Demandeurs"
        ordering = ['-date_inscription_user']
    
    def __str__(self):
        return f"{self.nom_user} {self.prenom_user} - {self.cin_user}"