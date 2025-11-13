from django.contrib import admin
from django.urls import path, include
from .views import home, about, contact
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Pages publiques
    path('', home, name='home'),
    path('about/', about, name='about_html'),
    path('contact/', contact, name='contact_html'),

    # Apps avec namespace
    path('evenements/', include(('GestionEvenements.urls', 'evenement'), namespace='evenement')),
    path('donors/', include(('GestionDoneurs.urls', 'doneurs'), namespace='doneurs')),
    path('volunteers/', include(('GestionVolontaires.urls'), namespace='volontaires')),
    path('sang/', include(('GestionSang.urls', 'sang'), namespace='sang')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
