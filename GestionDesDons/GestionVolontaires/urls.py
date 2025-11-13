from django.urls import path
from . import views

app_name = 'volontaires'  # <- indispensable pour le namespace

urlpatterns = [
    path('', views.volunteer, name='liste_volunteers'),  # liste des volontaires
    path('add/', views.ajouter_volunteer, name='ajouter_volunteer'),
    path('<int:pk>/edit/', views.edit_volunteer, name='edit_volunteer'),
    path('<int:pk>/delete/', views.delete_volunteer, name='delete_volunteer'),
    # Admin / Back-office
    path('admin/volunteers/', views.VolunteerListAdmin.as_view(), name='admin_volunteers'),
    path('admin/volunteers/add/', views.VolunteerCreateAdmin.as_view(), name='admin_volunteer_add'),
    path('admin/volunteers/<int:pk>/update/', views.VolunteerUpdateAdmin.as_view(), name='admin_volunteer_update'),
    path('admin/volunteers/<int:pk>/delete/', views.VolunteerDeleteAdmin.as_view(), name='admin_volunteer_delete'),
]
