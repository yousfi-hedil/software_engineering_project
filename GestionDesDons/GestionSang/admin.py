from django.contrib import admin
from .models import Sang

admin.site.site_title="Gestion des dons 25/26"
admin.site.site_header="DonVia"
admin.site.index_title="Stock : sang"
@admin.register(Sang)
class AdminSangModel(admin.ModelAdmin):
    list_display=("id_sang","groupe_sanguin","rhesus","quantite","status","date_collecte","date_expiration","lieu_stockage","a")
    ordering=("date_collecte",)
    list_filter=("groupe_sanguin",)
    search_fields=("groupe_sanguin","status") 
    date_hierarchy="date_collecte"
    fieldsets = (
        ("Information Générale", {
            "fields": ("id_sang", "groupe_sanguin","rhesus", "quantite", "status")
        }),
        ("Dates et Stockage", {
            "fields": ("date_collecte", "date_expiration", "lieu_stockage")
        }),
    )
    readonly_fields=("id_sang",)
    def a(self,objet):
        if objet.date_collecte and objet.date_expiration:
            return (objet.date_expiration-objet.date_collecte).days
        return "RAS"
    a.short_description="Duré de conservation (jours)"
    