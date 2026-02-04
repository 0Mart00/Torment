# Elérési út: D:\wwwroot\Kiss Edina\Torment\apps\catalog\views.py

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer, MindmapSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Hagyományos API végpont a termékek listázásához.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class MindmapAPIView(APIView):
    """
    Speciális végpont a Mindmap vizualizációhoz (Radial Layout algoritmus).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = MindmapSerializer(instance={})
        return Response(serializer.data)