# Elérési út: D:\wwwroot\Kiss Edina\Torment\apps\catalog\apps.py

from django.apps import AppConfig

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Ennek a névnek karakterre pontosan egyeznie kell 
    # a settings.py INSTALLED_APPS listájában szereplő névvel.
    name = 'catalog'