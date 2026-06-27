#!/usr/bin/env python
"""Script independiente para asignar imágenes de media/products/ a productos sin imagen.

Uso en VPS:
  cd /ruta/del/proyecto
  python fixtures/assign_images.py

Asigna los archivos .jpg de media/products/ (excluyendo copias con sufijo
auto-rename de Django) al campo image_main de los primeros productos activos
que no tengan imagen, ordenados por ID.

Idempotente: solo asigna a productos sin imagen; al re-ejecutar no duplica.
"""

import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo2026.settings')
django.setup()

from applications.products.models import Product


AUTO_RENAME_RE = re.compile(r'_[A-Za-z0-9]{7}\.jpg$', re.IGNORECASE)
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')


def get_image_files():
    """Retorna lista ordenada de archivos de imagen en media/products/,
    excluyendo copias con sufijo auto-rename de Django."""
    media_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'media', 'products')
    )

    if not os.path.isdir(media_dir):
        print(f'ERROR: No existe el directorio {media_dir}')
        return []

    files = [
        f for f in os.listdir(media_dir)
        if f.lower().endswith(IMAGE_EXTENSIONS)
        and not AUTO_RENAME_RE.search(f)
    ]

    return sorted(files)


def assign_images():
    image_files = get_image_files()
    print(f'Archivos de imagen encontrados (excluyendo duplicados): {len(image_files)}')

    if not image_files:
        print('No hay imágenes para asignar.')
        return

    products = list(
        Product.objects.filter(is_active=True, image_main__isnull=True)
        .order_by('id')
    )

    with_img = Product.objects.filter(is_active=True).exclude(
        image_main__isnull=True
    ).exclude(image_main__exact='').count()

    print(f'Productos activos sin imagen: {len(products)}')
    print(f'Productos activos con imagen: {with_img}')

    if not products:
        print('Todos los productos activos ya tienen imagen. Nada que asignar.')
        return

    assigned = 0
    for product, img_file in zip(products, image_files):
        product.image_main = f'products/{img_file}'
        product.save(update_fields=['image_main'])
        print(f'  Asignada {img_file} → Producto #{product.id:>4} ({product.name[:45]})')
        assigned += 1

    remaining_images = len(image_files) - assigned
    remaining_products = len(products) - assigned

    if remaining_images > 0:
        print(f'\n⚠ Quedaron {remaining_images} imágenes sin asignar (faltan productos sin imagen)')
    elif remaining_products > 0:
        print(f'\n⚠ Quedaron {remaining_products} productos sin imagen (faltan imágenes)')

    print(f'\nTotal: {assigned} imágenes asignadas correctamente.')


def main():
    print('=== Asignando imágenes a productos ===')
    assign_images()
    print('=== ¡Listo! ===')


if __name__ == '__main__':
    main()
