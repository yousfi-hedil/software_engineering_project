from django.urls import path
from . import views

urlpatterns = [
    path('', views.volunteer, name='liste_volunteers'),  # liste des volontaires
    path('add/', views.ajouter_volunteer, name='ajouter_volunteer'),
    path('<int:pk>/edit/', views.edit_volunteer, name='edit_volunteer'),
    path('<int:pk>/delete/', views.delete_volunteer, name='delete_volunteer'),
]
