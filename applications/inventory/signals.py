from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StockMovement


@receiver(post_save, sender=StockMovement)
def update_stock_on_movement(sender, instance, created, **kwargs):
    if not created:
        return
    product = instance.product
    if instance.movement_type == StockMovement.IN:
        product.stock += instance.quantity
    elif instance.movement_type == StockMovement.OUT:
        product.stock -= instance.quantity
    product.save(update_fields=['stock'])
