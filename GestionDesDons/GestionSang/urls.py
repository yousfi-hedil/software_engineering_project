from django.urls import path
from . import views

app_name = "sang"

urlpatterns = [
    # Front / Public
    path('', views.SangList.as_view(), name='liste_sangs'),
    path('ajouter/', views.SangCreate.as_view(), name='ajouter_sang'),
    path('<int:pk>/', views.SangDetails.as_view(), name='details_sang'),
    path('<int:pk>/modifier/', views.SangUpdate.as_view(), name='modifier_sang'),
    path('<int:pk>/supprimer/', views.SangDelete.as_view(), name='delete_sang'),

    # Back / Admin
    path('admin/sang/', views.SangListAdmin.as_view(), name='admin_sangs'),
    path('admin/sang/add/', views.SangCreateAdmin.as_view(), name='admin_sang_add'),
    path('admin/sang/<int:pk>/update/', views.SangUpdateAdmin.as_view(), name='admin_sang_update'),
    path('admin/sang/<int:pk>/delete/', views.SangDeleteAdmin.as_view(), name='admin_sang_delete'),
]
