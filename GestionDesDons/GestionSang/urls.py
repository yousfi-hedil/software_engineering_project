from django.urls import path
from .views import (
    SangList,
    SangDetails,
    SangCreate,
    SangUpdate,
    SangDelete,
)

urlpatterns = [
    path('', SangList.as_view(), name='liste_sangs'),  
    path('ajouter/', SangCreate.as_view(), name='ajouter_sang'),
    path('<int:pk>/', SangDetails.as_view(), name='details_sang'),
    path('<int:pk>/modifier/', SangUpdate.as_view(), name='modifier_sang'),
    path('sang/<int:pk>/supprimer/', SangDelete.as_view(), name='delete_sang'),
   
]
