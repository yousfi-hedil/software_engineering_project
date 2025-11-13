from django.urls import path
from . import views

app_name = "evenement"

urlpatterns = [
    # Front
    path('', views.EvenementList.as_view(), name='liste_evenements'),  
    path('ajouter/', views.EvenementCreate.as_view(), name='ajouter_evenement'),
    path('<int:pk>/', views.EvenementDetails.as_view(), name='details_evenement'),
    path('<int:pk>/modifier/', views.EvenementUpdate.as_view(), name='modifier_evenement'),
    path('<int:pk>/supprimer/', views.EvenementDelete.as_view(), name='delete_evenement'),
    
    # Back / Admin
    path('admin/events/', views.EvenementListAdmin.as_view(), name='admin_evenements'),
    path('admin/events/add/', views.EvenementCreateAdmin.as_view(), name='admin_evenement_add'),
    path('admin/events/<int:pk>/update/', views.EvenementUpdateAdmin.as_view(), name='admin_evenement_update'),
    path('admin/events/<int:pk>/delete/', views.EvenementDeleteAdmin.as_view(), name='admin_evenement_delete'),
]
