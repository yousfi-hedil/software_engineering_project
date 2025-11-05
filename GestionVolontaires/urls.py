from django.urls import path
from . import views

urlpatterns = [
    path('volunteer.html', views.volunteer, name='volunteer'),
    path('volunteers/', views.volunteer, name='volunteer'),
    path('volunteers/add/', views.ajouter_volunteer, name='ajouter_volunteer'),
    path('volunteers/<int:pk>/edit/', views.edit_volunteer, name='edit_volunteer'),
    path('volunteers/<int:pk>/delete/', views.delete_volunteer, name='delete_volunteer'),
]