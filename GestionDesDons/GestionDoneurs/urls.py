from django.urls import path
from . import views

app_name = 'doneurs'  # <-- ajoute ceci pour le namespace

urlpatterns = [
    # URLs publiques
    path('donors/', views.donors, name='liste_donneurs'),
    path('donors/add/', views.ajouter_donors, name='ajouter_donors'),
    path('donors/<int:pk>/edit/', views.edit_donor, name='edit_donor'),
    path('donors/<int:pk>/delete/', views.delete_donor, name='delete_donor'),

    # URLs Admin / Back-office
    path('admin/donors/', views.DonorListAdmin.as_view(), name='admin_donors'),
    path('admin/donors/add/', views.DonorCreateAdmin.as_view(), name='admin_donor_add'),
    path('admin/donors/<int:pk>/update/', views.DonorUpdateAdmin.as_view(), name='admin_donor_update'),
    path('admin/donors/<int:pk>/delete/', views.DonorDeleteAdmin.as_view(), name='admin_donor_delete'),
]
