from django.contrib import admin
from django.urls import path, include
from .views import home, about, contact
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Pages publiques
    path('', home, name='home'),                  # Accueil
    path('about/', about, name='about_html'),     # À propos
    path('contact/', contact, name='contact_html'),  # Contact

    # Apps
    path('evenements/', include('GestionEvenements.urls')),  # Événements
    path('donors/', include('GestionDoneurs.urls')),        # Donateurs
    path('volunteers/', include('GestionVolontaires.urls')), # Volontaires
    path('sang/', include('GestionSang.urls')),             # Sang
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
