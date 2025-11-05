from django.urls import path
from . import views

urlpatterns = [
    path('donors.html', views.donors, name='donors'),
    path('donors/', views.donors, name='donors'),
    path('donors/add/', views.ajouter_donors, name='ajouter_donors'),
    path('donors/<int:pk>/edit/', views.edit_donor, name='edit_donor'),
    path('donors/<int:pk>/delete/', views.delete_donor, name='delete_donor'),
]