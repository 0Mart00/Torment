# Elérési út: D:\wwwroot\Kiss Edina\Torment\apps\catalog\serializers.py

import math
from rest_framework import serializers
from .models import Product, Category
from analytics.services import ABPricingService

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    """
    Termék szériázó dinamikus árazással (A/B teszt támogatás).
    """
    current_price = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 
            'base_price', 'current_price', 'stock_quantity'
        ]

    def get_current_price(self, obj):
        request = self.context.get('request')
        user_id = "anonymous"
        if request and request.user.is_authenticated:
            user_id = request.user.id
        elif request and request.session:
            user_id = request.session.session_key or "anonymous"
            
        return ABPricingService.calculate_price(obj, user_id)

class MindmapSerializer(serializers.Serializer):
    """
    Radial Layout algoritmus a Mindmap vizualizációhoz.
    Ez a rész hiányzott a fájlból, ami az ImportError-t okozta.
    """
    nodes = serializers.SerializerMethodField()

    def get_nodes(self, obj):
        nodes = []
        # Központi Node (Root)
        nodes.append({'id': 'root', 'label': 'Digitális Erőd', 'type': 'category', 'x': 0, 'y': 0})
        
        categories = list(Category.objects.all())
        cat_count = len(categories)
        
        for i, cat in enumerate(categories):
            # Kategóriák elrendezése körben (Sugár: 350)
            angle = (2 * math.pi * i) / cat_count if cat_count > 0 else 0
            cat_x = 350 * math.cos(angle)
            cat_y = 350 * math.sin(angle)
            
            nodes.append({
                'id': f'cat-{cat.id}',
                'label': cat.name,
                'type': 'category',
                'x': cat_x,
                'y': cat_y,
                'parent': 'root'
            })
            
            # Termékek elrendezése a kategória körül (Sugár: 200)
            products = list(Product.objects.filter(category=cat))
            p_count = len(products)
            for j, prod in enumerate(products):
                # Kis eltérés az alapszögben, hogy ne fedjék egymást
                p_angle = angle + ((j - p_count/2) * 0.4)
                nodes.append({
                    'id': f'prod-{prod.id}',
                    'label': prod.name,
                    'type': 'product',
                    # Dinamikus árképzés itt is érvényesíthető ha szükséges
                    'price': float(prod.base_price),
                    'stock': prod.stock_quantity,
                    'x': cat_x + 200 * math.cos(p_angle),
                    'y': cat_y + 200 * math.sin(p_angle),
                    'parent': f'cat-{cat.id}'
                })
        return nodes