import os

from django.conf import settings
from django.core.management.base import BaseCommand

from applications.products.models import Product


class Command(BaseCommand):
    help = 'Asigna las imágenes de media/products/ a los primeros 18 productos sin imagen'

    def handle(self, *args, **options):
        media_products = settings.MEDIA_ROOT / 'products'
        images = sorted([f for f in os.listdir(media_products) if f.lower().endswith('.jpg')])

        if not images:
            self.stdout.write(self.style.WARNING('No se encontraron imágenes en media/products/'))
            return

        products = Product.objects.filter(image_main='').order_by('pk')[:len(images)]

        if not products:
            self.stdout.write(self.style.WARNING('No hay productos sin imagen asignada'))
            return

        for product, img in zip(products, images):
            product.image_main = f'products/{img}'
            product.save(update_fields=['image_main'])
            self.stdout.write(f'  #{product.pk:>3} {product.name:<40} -> {img}')

        self.stdout.write(self.style.SUCCESS(
            f'Asignadas {len(products)} imágenes a los primeros {len(products)} productos.'
        ))
