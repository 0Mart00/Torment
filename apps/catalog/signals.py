from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Product
from apps.analytics.models import AuditLog
from django.contrib.contenttypes.models import ContentType

@receiver(pre_save, sender=Product)
def capture_product_changes(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            instance._old_instance = old_instance
        except Product.DoesNotExist:
            instance._old_instance = None

@receiver(post_save, sender=Product)
def log_product_changes(sender, instance, created, **kwargs):
    if created:
        return # Create logikát külön is lehet kezelni

    if hasattr(instance, '_old_instance'):
        old = instance._old_instance
        changes = {}
        
        # Figyelt mezők
        monitored_fields = ['base_price', 'stock_quantity']
        
        for field in monitored_fields:
            old_val = getattr(old, field)
            new_val = getattr(instance, field)
            if old_val != new_val:
                changes[field] = {'old': str(old_val), 'new': str(new_val)}
        
        if changes:
            AuditLog.objects.create(
                content_object=instance,
                action='UPDATE',
                changes=changes,
                # Actor beszerzése middleware-ből vagy thread local-ból (pl. django-cuser) ajánlott
            )