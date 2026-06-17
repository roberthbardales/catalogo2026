from django.db import models
from model_utils.models import TimeStampedModel

from applications.products.models import Product


class QuotationRequest(TimeStampedModel):
    PENDIENTE = 'P'
    APROBADA = 'A'
    RECHAZADA = 'R'
    COMPLETADA = 'C'

    STATUS_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (APROBADA, 'Aprobada'),
        (RECHAZADA, 'Rechazada'),
        (COMPLETADA, 'Completada'),
    ]

    customer_name = models.CharField('Nombre', max_length=120)
    customer_email = models.EmailField('Correo electrónico')
    customer_phone = models.CharField('Teléfono', max_length=15)
    notes = models.TextField('Notas', blank=True)
    status = models.CharField('Estado', max_length=1, choices=STATUS_CHOICES, default=PENDIENTE)

    class Meta:
        verbose_name = 'Solicitud de cotización'
        verbose_name_plural = 'Solicitudes de cotización'
        ordering = ['-created']

    def __str__(self):
        return f'Cotización #{self.pk} — {self.customer_name}'


class QuotationItem(TimeStampedModel):
    quotation = models.ForeignKey(
        QuotationRequest, on_delete=models.CASCADE,
        related_name='items', verbose_name='Cotización'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='quotation_items', verbose_name='Producto'
    )
    product_name = models.CharField('Nombre del producto', max_length=180)
    product_sku = models.CharField('SKU', max_length=80)
    quantity = models.PositiveIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item de cotización'
        verbose_name_plural = 'Items de cotización'
        ordering = ['pk']

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'
