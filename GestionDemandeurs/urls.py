from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_demandeur, name='add_demandeur'),
    path('list/', views.list_demandeur, name='list_demandeur'),
    path('detail/<int:pk>/', views.detail_demandeur, name='detail_demandeur'),
    path('edit/<int:pk>/', views.edit_demandeur, name='edit_demandeur'),
    path('delete/<int:pk>/', views.delete_demandeur, name='delete_demandeur'),
    # This will show all demandeurs (no pk)
    path('detail/', views.all_demandeurs, name='all_demandeurs'),
]
