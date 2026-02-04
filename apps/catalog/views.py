# Elérési út: D:\wwwroot\Kiss Edina\Torment\apps\catalog\views.py

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer, MindmapSerializer
from .models import Category, Product
import math

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Hagyományos API végpont a termékek listázásához.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class MindmapAPIView(APIView):
    permission_classes = [] # Teszteléshez mindenki láthatja

    def get(self, request):
        nodes = []
        # Központi elem (Root)
        nodes.append({"id": "root", "label": "Mag", "type": "core", "x": 0, "y": 0})

        categories = Category.objects.all()
        # Egyszerű körkörös elrendezés generálása a kategóriáknak
        for i, cat in enumerate(categories):
            angle = (i / max(len(categories), 1)) * 2 * math.pi
            radius = 300
            cat_x = int(math.cos(angle) * radius)
            cat_y = int(math.sin(angle) * radius)
            
            nodes.append({
                "id": f"c{cat.id}",
                "label": cat.name,
                "type": "category",
                "x": cat_x,
                "y": cat_y,
                "parent": "root"
            })

            # Termékek a kategórián belül
            products = Product.objects.filter(category=cat)
            for j, prod in enumerate(products):
                p_angle = angle + (j + 1) * 0.2 # Kicsit eltolva a kategóriától
                p_radius = 600
                nodes.append({
                    "id": f"p{prod.id}",
                    "label": prod.name,
                    "type": "product",
                    "price": f"{prod.price} Ft",
                    "stock": prod.stock,
                    "img": prod.image.url if prod.image else None,
                    "x": int(math.cos(p_angle) * p_radius),
                    "y": int(math.sin(p_angle) * p_radius),
                    "parent": f"c{cat.id}"
                })

        return Response({"nodes": nodes})