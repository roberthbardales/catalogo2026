#!/usr/bin/env python
"""Script independiente para sembrar datos en la BD.

Uso en VPS:
  cd /ruta/del/proyecto
  python fixtures/seed_data.py

Crea:
  - 10 categorías
  - 10 marcas
  - 100 productos (electrónica)
  - 3 usuarios: admin, ventas, cliente
"""

import os
import sys
import random
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo2026.settings')
django.setup()

from applications.products.models import Category, Brand, Product
from applications.users.models import User


CATEGORIES = [
    {'name': 'Laptops', 'prefix': 'LAP', 'desc': 'Laptops y notebooks'},
    {'name': 'Audífonos', 'prefix': 'AUD', 'desc': 'Audífonos y auriculares'},
    {'name': 'Periféricos', 'prefix': 'PER', 'desc': 'Teclados, mice y accesorios'},
    {'name': 'Accesorios', 'prefix': 'ACC', 'desc': 'Accesorios diversos'},
    {'name': 'Almacenamiento', 'prefix': 'ALM', 'desc': 'Discos duros, SSDs y memorias'},
    {'name': 'Monitores', 'prefix': 'MON', 'desc': 'Monitores y pantallas'},
    {'name': 'Tablets', 'prefix': 'TAB', 'desc': 'Tablets y lectores'},
    {'name': 'Cargadores y Cables', 'prefix': 'CAB', 'desc': 'Cargadores, cables y adaptadores'},
    {'name': 'Componentes', 'prefix': 'COM', 'desc': 'Componentes de PC'},
    {'name': 'Parlantes y Audio', 'prefix': 'PAR', 'desc': 'Parlantes y equipos de audio'},
]

BRANDS = [
    'Samsung', 'Apple', 'Sony', 'LG', 'Dell',
    'HP', 'Lenovo', 'ASUS', 'Microsoft', 'Logitech',
]

PRODUCT_NAMES = {
    'Laptops': [
        'Laptop {brand} Ultralight {n}15"', 'Laptop {brand} ProBook {n}14"',
        'Laptop {brand} Gamer {n}17"', 'Laptop {brand} Business {n}13"',
        'Laptop {brand} Slim {n}15"', 'Laptop {brand} Edge {n}14"',
        'Laptop {brand} Workstation {n}17"', 'Laptop {brand} Air {n}13"',
        'Laptop {brand} Studio {n}16"', 'Laptop {brand} Go {n}11"',
    ],
    'Audífonos': [
        'Auriculares {brand} Bluetooth {n}', 'Audífonos {brand} Pro {n}',
        'Headset {brand} Gamer {n}', 'Auriculares {brand} In-Ear {n}',
        'Audífonos {brand} Cancelación Ruido {n}', 'Headphones {brand} Studio {n}',
        'Auriculares {brand} Deportivos {n}', 'Audífonos {brand} Wireless {n}',
        'Headset {brand} Office {n}', 'Auriculares {brand} Hi-Fi {n}',
    ],
    'Periféricos': [
        'Teclado {brand} Mecánico {n}', 'Mouse {brand} Óptico {n}',
        'Teclado {brand} Inalámbrico {n}', 'Mouse {brand} Gamer {n}',
        'Teclado {brand} Ergonómico {n}', 'Mousepad {brand} XL {n}',
        'Webcam {brand} HD {n}', 'Teclado {brand} Slim {n}',
        'Mouse {brand} Bluetooth {n}', 'Combo Teclado+Mouse {brand} {n}',
    ],
    'Accesorios': [
        'Hub USB {brand} 7 puertos {n}', 'Soporte laptop {brand} Ajustable {n}',
        'Funda laptop {brand} {n}"', 'Mochila {brand} Anti-Impacto {n}',
        'Base refrigerante {brand} {n}', 'Organizador cables {brand} {n}',
        'Soporte monitor {brand} {n}', 'Kit limpieza {brand} {n}',
        'Adaptador {brand} USB-C {n}', 'Guante antiestático {brand} {n}',
    ],
    'Almacenamiento': [
        'SSD {brand} 240GB {n}', 'SSD {brand} 480GB {n}',
        'SSD {brand} 1TB {n}', 'SSD {brand} NVMe 500GB {n}',
        'SSD {brand} NVMe 1TB {n}', 'Disco Duro {brand} 1TB {n}',
        'Disco Duro {brand} 2TB {n}', 'Memoria USB {brand} 64GB {n}',
        'Memoria USB {brand} 128GB {n}', 'Tarjeta SD {brand} 128GB {n}',
    ],
    'Monitores': [
        'Monitor {brand} 22" Full HD {n}', 'Monitor {brand} 24" IPS {n}',
        'Monitor {brand} 27" 4K {n}', 'Monitor {brand} 32" Curvo {n}',
        'Monitor {brand} 21" Office {n}', 'Monitor {brand} 28" 4K {n}',
        'Monitor {brand} 24" Gamer 144Hz {n}', 'Monitor {brand} 27" 2K {n}',
        'Monitor {brand} 34" Ultrawide {n}', 'Monitor {brand} 19" Básico {n}',
    ],
    'Tablets': [
        'Tablet {brand} 8" WiFi {n}', 'Tablet {brand} 10" HD {n}',
        'Tablet {brand} 11" Pro {n}', 'Tablet {brand} 7" Compact {n}',
        'Tablet {brand} 10" 4G {n}', 'Tablet {brand} 12" Ultra {n}',
        'E-Reader {brand} 6" {n}', 'E-Reader {brand} 7" Retroiluminado {n}',
        'Tablet {brand} 9" Kids {n}', 'Tablet {brand} 10" Premium {n}',
    ],
    'Cargadores y Cables': [
        'Cargador USB-C {brand} 65W {n}', 'Cargador USB-C {brand} 30W {n}',
        'Cable USB-C {brand} 1m {n}', 'Cable USB-C {brand} 2m {n}',
        'Cargador inalámbrico {brand} {n}', 'Cable HDMI {brand} 1.5m {n}',
        'Cable HDMI {brand} 3m {n}', 'Adaptador corriente {brand} {n}',
        'Cable Ethernet {brand} 5m {n}', 'Power Bank {brand} 10000mAh {n}',
    ],
    'Componentes': [
        'Procesador {brand} Core {n}', 'Placa madre {brand} ATX {n}',
        'Memoria RAM {brand} 8GB DDR4 {n}', 'Memoria RAM {brand} 16GB DDR4 {n}',
        'Fuente poder {brand} 600W {n}', 'Fuente poder {brand} 750W {n}',
        'Tarjeta gráfica {brand} {n}', 'Disipador CPU {brand} {n}',
        'Ventilador case {brand} 120mm {n}', 'Case PC {brand} ATX {n}',
    ],
    'Parlantes y Audio': [
        'Parlante {brand} Bluetooth Portátil {n}', 'Parlante {brand} 2.1 {n}',
        'Barra sonido {brand} {n}"', 'Parlante {brand} Bluetooth 5.0 {n}',
        'Subwoofer {brand} {n}"', 'Parlante {brand} USB {n}',
        'Micrófono {brand} USB {n}', 'Micrófono {brand} Condenser {n}',
        'Parlante {brand} Party {n}', 'Kit audio {brand} 5.1 {n}',
    ],
}


USERS = [
    {
        'email': 'admin@admin.com',
        'password': 'admin123',
        'first_name': 'Admin',
        'last_name': 'Principal',
        'occupation': '0',
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'email': 'ventas@ventas.com',
        'password': 'ventas123',
        'first_name': 'Ventas',
        'last_name': 'User',
        'occupation': '1',
        'is_staff': True,
    },
    {
        'email': 'cliente@cliente.com',
        'password': 'cliente123',
        'first_name': 'Cliente',
        'last_name': 'Test',
        'occupation': '2',
    },
]


def seed_products():
    created_cats = 0
    created_brands = 0
    created_products = 0
    skipped_products = 0

    categories = {}
    for cat_data in CATEGORIES:
        cat, was_created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['desc']},
        )
        if was_created:
            created_cats += 1
        categories[cat_data['name']] = cat

    brand_objs = []
    for brand_name in BRANDS:
        brand, was_created = Brand.objects.get_or_create(
            name=brand_name,
            defaults={'description': f'Marca {brand_name}'},
        )
        if was_created:
            created_brands += 1
        brand_objs.append(brand)

    for cat_data in CATEGORIES:
        cat_name = cat_data['name']
        prefix = cat_data['prefix']
        cat = categories[cat_name]
        names = PRODUCT_NAMES[cat_name]

        for i in range(10):
            brand = random.choice(brand_objs)
            model_num = random.randint(100, 999)
            name = random.choice(names).format(brand=brand.name, n=model_num)
            sku = f'{prefix}-{i + 1:03d}'

            if Product.objects.filter(sku=sku).exists():
                skipped_products += 1
                continue

            Product.objects.create(
                name=name,
                sku=sku,
                price=random.randint(1000, 50000),
                stock=random.randint(0, 100),
                category=cat,
                brand=brand,
                description=f'{name} — Producto de alta calidad ideal para tus necesidades diarias.',
                short_description=f'{brand.name} {cat_name.lower()} modelo {model_num}.',
                is_active=True,
            )
            created_products += 1

    print(f'Categorías: {created_cats} creadas')
    print(f'Marcas: {created_brands} creadas')
    print(f'Productos: {created_products} creados ({skipped_products} omitidos por SKU duplicado)')


def seed_users():
    created = 0
    skipped = 0
    for data in USERS:
        email = data['email']
        if User.objects.filter(email=email).exists():
            skipped += 1
            continue
        password = data.pop('password')
        user = User(**data)
        user.set_password(password)
        user.save()
        created += 1
    print(f'Usuarios: {created} creados ({skipped} omitidos por existir)')


def main():
    print('=== Sembrando datos ===')
    seed_products()
    seed_users()
    print('=== ¡Listo! ===')


if __name__ == '__main__':
    main()
