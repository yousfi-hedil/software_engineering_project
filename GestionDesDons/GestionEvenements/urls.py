from django.urls import path
from .views import (
    EvenementList,
    EvenementDetails,
    EvenementCreate,
    EvenementUpdate,
    EvenementDelete,
)

urlpatterns = [
    path('', EvenementList.as_view(), name='liste_evenements'),  
    path('ajouter/', EvenementCreate.as_view(), name='ajouter_evenement'),
    path('<int:pk>/', EvenementDetails.as_view(), name='details_evenement'),
    path('<int:pk>/modifier/', EvenementUpdate.as_view(), name='modifier_evenement'),
    path('evenement/<int:pk>/supprimer/', EvenementDelete.as_view(), name='delete_evenement'),
]
