# Elérési út: D:\wwwroot\Kiss Edina\Torment\config\urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # KRITIKUS JAVÍTÁS: Mivel az 'apps' mappa a sys.path-ban van, 
    # tilos az 'apps.' előtag használata! Csak 'catalog.urls'.
    path('api/catalog/', include('catalog.urls')),
]