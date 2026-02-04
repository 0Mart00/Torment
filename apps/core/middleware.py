import hashlib
import json
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status

class IdempotencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Csak a módosító metódusokra figyelünk
        if request.method not in ['POST', 'PATCH', 'PUT']:
            return self.get_response(request)

        key = request.headers.get('Idempotency-Key')
        if not key:
            return self.get_response(request)

        # Kulcs generálása: Header + User ID + URL
        user_part = str(request.user.id) if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
        cache_key = f"idempotency:{user_part}:{key}"

        # 1. Ellenőrzés: Van-e már tárolt válasz?
        stored_response = cache.get(cache_key)
        if stored_response:
            return JsonResponse(stored_response['data'], status=stored_response['status'])

        # 2. Zárolás: Éppen feldolgozás alatt áll?
        lock_key = f"{cache_key}:lock"
        if cache.get(lock_key):
             return JsonResponse(
                 {"error": "Processing in progress"}, 
                 status=status.HTTP_409_CONFLICT
             )

        # 3. Feldolgozás indítása (Lock set)
        cache.set(lock_key, "LOCKED", timeout=60) 

        response = self.get_response(request)

        # 4. Siker esetén válasz tárolása (24 órára)
        if 200 <= response.status_code < 300:
            response_data = {
                'status': response.status_code,
                'data': json.loads(response.content) if response.content else {}
            }
            cache.set(cache_key, response_data, timeout=60*60*24)
        
        # Lock feloldása
        cache.delete(lock_key)
        
        return response