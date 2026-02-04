from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F

class ProductViewSet(viewsets.ModelViewSet):
    # ... querysets ...
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get('q')
        
        if query:
            # Webshop-specifikus keresési logika
            search_query = SearchQuery(query, config='hungarian')
            
            # Rangsorolás: A címben való egyezés többet ér (A), mint a leírásban
            qs = qs.annotate(
                rank=SearchRank(F('search_vector'), search_query)
            ).filter(search_vector=search_query).order_by('-rank')
            
        return qs