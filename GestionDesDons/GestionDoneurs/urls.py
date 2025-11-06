from django.urls import path
from . import views

urlpatterns = [
    path('donors/', views.donors, name='liste_donneurs'),  # ← ici
    path('donors/add/', views.ajouter_donors, name='ajouter_donors'),
    path('donors/<int:pk>/edit/', views.edit_donor, name='edit_donor'),
    path('donors/<int:pk>/delete/', views.delete_donor, name='delete_donor'),
]
