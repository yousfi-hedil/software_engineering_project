from django.contrib import admin
from .models import Volunteer

# ==========================
# Admin Volunteer
# ==========================
@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'prenom', 'email', 'telephone', 'ville', 'sexe',
        'disponibilite', 'date_inscription', 'created_at',
    )
    search_fields = (
        'nom', 'prenom', 'email', 'telephone', 'ville', 'specialite',
    )
    list_filter = (
        'sexe', 'disponibilite', 'ville', 'date_inscription', 'created_at',
    )
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
