import random
from django.core.cache import cache

class ABPricingService:
    @staticmethod
    def get_user_segment(user_id):
        """
        Visszaadja a felhasználó szegmensét ('A' vagy 'B').
        Redis cache-t használ a konzisztencia érdekében (Sticky Session).
        """
        cache_key = f"ab_segment:{user_id}"
        segment = cache.get(cache_key)
        
        if not segment:
            # Véletlenszerű elosztás 50-50%
            segment = 'B' if random.random() > 0.5 else 'A'
            cache.set(cache_key, segment, timeout=60*60*24*7) # 1 hétig érvényes
        
        return segment

    @staticmethod
    def calculate_price(product, user_id):
        segment = ABPricingService.get_user_segment(user_id)
        
        # 'A' csoport: Alapár (Kontroll csoport)
        if segment == 'A':
            return product.base_price
            
        # 'B' csoport: Dinamikus árképzés (Kísérleti csoport)
        # Algoritmus: Ha a készlet < 10, ár + 15% (Scarcity Principle)
        elif segment == 'B':
            if product.stock_quantity < 10:
                return product.base_price * 1.15
            else:
                return product.base_price
        
        return product.base_price