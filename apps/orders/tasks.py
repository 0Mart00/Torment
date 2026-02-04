# apps/orders/tasks.py
from celery import shared_task
from django.db import transaction

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def process_stripe_webhook(event_data):
    """
    Stripe webhook aszinkron feldolgozása.
    Hiba esetén exponenciális visszatartással próbálkozik újra.
    """
    event_type = event_data['type']
    if event_type == 'payment_intent.succeeded':
        with transaction.atomic():
            # Rendelés státusz frissítése
            # Számla generálás PDF-ben
            # Email küldés
            pass