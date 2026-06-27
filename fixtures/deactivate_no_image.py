#!/usr/bin/env python
"""Desactiva productos activos que no tienen imagen asignada.

Uso en VPS:
  cd /ruta/del/proyecto
  python fixtures/deactivate_no_image.py
"""

import os
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo2026.settings')
django.setup()

from django.db.models import Q

from applications.products.models import Product


def deactivate():
    no_img_q = Q(image_main__isnull=True) | Q(image_main__exact='')

    count = Product.objects.filter(is_active=True).filter(no_img_q).update(is_active=False)
    print(f'Productos desactivados por no tener imagen: {count}')


def main():
    print('=== Desactivando productos sin imagen ===')
    deactivate()
    print('=== ¡Listo! ===')


if __name__ == '__main__':
    main()
