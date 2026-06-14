from django.db import models
from model_utils.models import TimeStampedModel


class StockMovement(TimeStampedModel):
    IN = 'IN'
    OUT = 'OUT'

    MOVEMENT_TYPE_CHOICES = (
        (IN, 'Entrada'),
        (OUT, 'Salida'),
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='stock_movements',
    )
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
    )

    class Meta:
        verbose_name = 'Movimiento de stock'
        verbose_name_plural = 'Movimientos de stock'
        ordering = ['-created']

    def __str__(self):
        return f'{self.product.name} - {self.get_movement_type_display()} - {self.quantity}'
