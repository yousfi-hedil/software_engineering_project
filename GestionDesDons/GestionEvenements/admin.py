'''
from django.contrib import admin
from .models import Evenement

admin.site.site_title="Gestion des dons 25/26"
admin.site.site_header="Gestion des événements"
admin.site.index_title="Nos événements"
@admin.register(Evenement)
class AdminEvenementModel(admin.ModelAdmin):
    list_display=("id_evenement","titre","description","date_debut","date_fin","nb_participants","statut","lieu_evenement","a")
    ordering=("date_debut",)
    list_filter=("statut",)
    search_fields=("titre","statut") 
    date_hierarchy="date_debut"
    fieldsets = (
        ("Information Générale", {
            "fields": ("id_evenement", "titre","description", "nb_participants", "statut")
        }),
        ("Dates et Stockage", {
            "fields": ("date_debut", "date_fin", "lieu_evenement")
        }),
    )
    readonly_fields=("id_evenement",)
    def a(self,objet):
        if objet.date_debut and objet.date_fin:
            return (objet.date_fin-objet.date_debut).days
        return "RAS"
    a.short_description="Duré de l'événement (jours)"
    '''