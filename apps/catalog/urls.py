# Elérési út: D:\wwwroot\Kiss Edina\Torment\apps\catalog\urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MindmapAPIView, ProductViewSet

# Router használata a ModelViewSet-hez (automatikus list és detail URL-ek)
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Router által generált útvonalak: /api/catalog/products/
    path('', include(router.urls)),
    
    # Egyedi Mindmap végpont: /api/catalog/mindmap/
    path('mindmap/', MindmapAPIView.as_view(), name='api-mindmap'),
]