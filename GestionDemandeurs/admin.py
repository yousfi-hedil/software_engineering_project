from django.contrib import admin
from .models import Demandeur

@admin.register(Demandeur)
class DemandeurAdmin(admin.ModelAdmin):
    list_display = ['cin_user', 'nom_user', 'prenom_user', 'email_user', 'institution', 'date_inscription_user']
    list_filter = ['institution', 'sexe_user', 'date_inscription_user']
    search_fields = ['nom_user', 'prenom_user', 'cin_user', 'email_user']
    ordering = ['-date_inscription_user']