# 🛒 Catálogo 2026

**Plataforma de catálogo y cotización en línea** para [Solutions Mech Perú](https://solutionsmechperu.com) — un sistema completo de e-commerce B2B que permite a los clientes explorar productos, agregar items a una cotización y enviar solicitudes directamente desde la web.

![Django](https://img.shields.io/badge/Django-3.2-blue?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-green?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge)

---

## 📋 Tabla de contenidos

- [Descripción](#-descripción)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Funcionalidades](#-funcionalidades)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Requisitos previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Variables de entorno](#-variables-de-entorno)
- [Ejecución en desarrollo](#-ejecución-en-desarrollo)
- [Población de datos de prueba](#-población-de-datos-de-prueba)
- [Despliegue en producción](#-despliegue-en-producción)
- [Arquitectura](#-arquitectura)
- [Licencia](#-licencia)

---

## 📖 Descripción

**Catálogo 2026** es una aplicación web desarrollada con Django que funciona como portal de productos y generador de cotizaciones para Solutions Mech Perú, una empresa de tecnología con sede en Ate, Lima.

El sistema permite a los visitantes navegar un catálogo completo de productos tecnológicos (laptops, audífonos, periféricos, redes, etc.), filtrar por categorías y marcas, buscar en tiempo real, y agregar productos a una cotización que se envía por correo electrónico al equipo de ventas.

Los usuarios internos (administradores y vendedores) cuentan con un panel de administración completo para gestionar productos, categorías, marcas, movimientos de inventario y cotizaciones recibidas.

---

## 🛠 Tecnologías utilizadas

### Backend
| Tecnología | Versión | Propósito |
|---|---|---|
| **Django** | 3.2.25 | Framework web principal |
| **PostgreSQL** | 14+ | Base de datos relacional |
| **django-environ** | 0.11.2 | Gestión de variables de entorno |
| **django-model-utils** | 5.0.0 | Modelos con timestamps automáticos |
| **Pillow** | 9.5.0 | Procesamiento de imágenes |
| **psycopg2-binary** | 2.9.9 | Adaptador PostgreSQL |

### Frontend
| Tecnología | Propósito |
|---|---|
| **Bootstrap 5.3** | Framework CSS responsivo |
| **Font Awesome 6.5** | Iconografía |
| **JavaScript vanilla** | AJAX, buscador en tiempo real, carrito |
| **HTML5 / CSS3** | Estructura y estilos |

### Infraestructura
| Componente | Detalle |
|---|---|
| **Correo** | SMTP Gmail (notificaciones de cotización) |
| **WhatsApp** | Integración directa con API de mensajería |
| **Imágenes** | Servidas por Django en desarrollo, media files en producción |

---

## 🎯 Funcionalidades

### 🌐 Portal público
- **Catálogo de productos** con grid responsivo y paginación
- **Buscador en tiempo real** (AJAX) en el header — resultados instantáneos con imagen, precio y stock
- **Filtros dinámicos** por categoría, marca y búsqueda combinada
- **Detalle de producto** con galería de imágenes (lightbox), especificaciones técnicas, precio de oferta y productos relacionados
- **Cotización rápida** — carrito en sesión con botones de agregar/quitar, formulario de envío y confirmación
- **Páginas informativas**: Nosotros, Categorías, Marcas, Garantía, Contacto
- **Franja de ofertas** animada en la página principal
- **Botón flotante de WhatsApp** con opciones de consulta

### 🔐 Panel de administración
- **Dashboard** con KPIs en tiempo real: productos activos, categorías, marcas, cotizaciones, stock bajo, sin stock
- **Gestión de productos** — CRUD completo con imágenes, especificaciones técnicas, precios y stock
- **Gestión de categorías y marcas** — CRUD con activación/desactivación
- **Inventario** — registro de movimientos de stock (entradas/salidas) con actualización automática del stock del producto
- **Cotizaciones** — listado, detalle y seguimiento de solicitudes de clientes
- **Gestión de usuarios** — crear, editar, activar/desactivar, resetear contraseñas
- **Cambiar contraseña** — formulario seguro dentro del panel

### 👥 Sistema de usuarios
- **3 roles con permisos diferenciados**:
  - 🔴 **Administrador** — acceso total al panel y administración
  - 🟡 **Ventas** — acceso a dashboard, cotizaciones e inventario
  - 🔵 **Cliente** — acceso a perfil
- **Autenticación por email** (no por username)
- **Login / Logout** con redirección automática

### 📧 Notificaciones por correo
- Las cotizaciones enviadas generan un email con la tabla de productos, subtotales y datos del cliente
- Correo enviado al cliente y en copia (CC) al equipo de ventas

---

## 📁 Estructura del proyecto

```
catalogo2026/
├── applications/                  # Apps Django
│   ├── home/                      # Página principal, catálogo público, APIs
│   ├── products/                  # Modelo de productos, categorías, marcas
│   ├── quotations/                # Sistema de cotizaciones y carrito
│   ├── inventory/                 # Gestión de movimientos de stock
│   ├── users/                     # Usuarios, autenticación, permisos
│   └── procesors.py               # Context processors (WhatsApp, categorías, carrito)
├── catalogo2026/                  # Configuración del proyecto Django
│   ├── settings.py                # Settings principales
│   ├── urls.py                    # URL routing raíz
│   ├── wsgi.py                    # WSGI para producción
│   └── asgi.py                    # ASGI
├── templates/                     # Templates HTML (Django Template Language)
│   ├── base.html                  # Plantilla raíz
│   ├── home/                      # Templates del portal público
│   ├── products/                  # Templates de administración de productos
│   ├── quotations/                # Templates de cotizaciones
│   ├── inventory/                 # Templates de inventario
│   ├── users/                     # Templates de autenticación y panel
│   └── include/                   # Componentes reutilizables (header, footer, sidebar)
├── static/                        # Archivos estáticos (CSS, imágenes)
│   ├── css/                       # Hojas de estilo
│   └── img/                       # Imágenes estáticas
├── media/                         # Archivos subidos por usuarios (imágenes)
├── fixtures/                      # Scripts de seed y datos iniciales
│   ├── seed_data.py               # Script de población de datos
│   ├── seed_productos.json        # Fixture JSON (categorías, marcas, productos)
│   ├── assign_images.py           # Asignador de imágenes a productos
│   └── deactivate_no_image.py     # Desactiva productos sin imagen
├── .env                           # Variables de entorno (no versionado)
├── .gitignore
├── requirements.txt               # Dependencias Python
├── manage.py                      # CLI de Django
├── activar.bat                    # Script para activar venv (Windows)
└── README.md
```

---

## 🧩 Modelos principales

### Usuarios (`users.User`)
| Campo | Tipo | Descripción |
|---|---|---|
| `email` | EmailField | Identificador único (login) |
| `first_name` / `last_name` | CharField | Nombre y apellido |
| `occupation` | Choice | Administrador / Ventas / Cliente |
| `gender` | Choice | Masculino / Femenino / Otro |
| `phone` | CharField | Teléfono |

### Productos (`products.Product`)
| Campo | Tipo | Descripción |
|---|---|---|
| `name` | CharField | Nombre del producto |
| `sku` | CharField | Código único de inventario |
| `price` | DecimalField | Precio regular |
| `sale_price` | DecimalField | Precio de oferta (opcional) |
| `stock` | PositiveIntegerField | Stock disponible |
| `category` | ForeignKey | Categoría del producto |
| `brand` | ForeignKey | Marca del producto |
| `image_main` | ImageField | Imagen principal |
| `is_active` | BooleanField | Producto visible en catálogo |

### Cotizaciones (`quotations.QuotationRequest`)
| Campo | Tipo | Descripción |
|---|---|---|
| `customer_name` | CharField | Nombre del cliente |
| `customer_email` | EmailField | Correo electrónico |
| `customer_phone` | CharField | Teléfono |
| `notes` | TextField | Notas adicionales |
| *items* | RelatedManager | Items de la cotización |

### Inventario (`inventory.StockMovement`)
| Campo | Tipo | Descripción |
|---|---|---|
| `product` | ForeignKey | Producto afectado |
| `movement_type` | Choice | Entrada (IN) / Salida (OUT) |
| `quantity` | PositiveIntegerField | Cantidad movida |
| `created_by` | ForeignKey | Usuario que registró el movimiento |

---

## 📦 Requisitos previos

- **Python** 3.10 o superior
- **PostgreSQL** 12 o superior
- **pip** (gestor de paquetes)
- **Git** (para clonar el repositorio)

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/catalogo2026.git
cd catalogo2026
```

### 2. Crear y activar el entorno virtual

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

> 💡 En Windows también puedes ejecutar `activar.bat` desde la raíz del proyecto.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos

```bash
# Conectar a PostgreSQL y crear la base de datos
psql -U postgres
CREATE DATABASE db_catalogo2026;
CREATE USER tu_usuario WITH PASSWORD 'tu_password';
ALTER ROLE tu_usuario SET client_encoding TO 'utf8';
ALTER ROLE tu_usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE tu_usuario SET timezone TO 'America/Lima';
GRANT ALL PRIVILEGES ON DATABASE db_catalogo2026 TO tu_usuario;
\q
```

### 5. Configurar variables de entorno

Crea el archivo `.env` en la raíz del proyecto (ver [Variables de entorno](#-variables-de-entorno)).

### 6. Aplicar migraciones

```bash
python manage.py migrate
```

### 7. Crear usuario administrador

```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor

```bash
python manage.py runserver
```

Accede a: **http://127.0.0.1:8000/**

---

## 🔐 Variables de entorno

El archivo `.env` debe colocarse en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=db_catalogo2026
DB_USER=tu_usuario
DB_PASSWORD=tu-password-aqui
DB_HOST=localhost
DB_PORT=5432

# Email (SMTP Gmail)
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password-de-gmail
```

> ⚠️ **Importante:** Nunca subas el archivo `.env` a repositorios públicos. Ya está incluido en `.gitignore`.

---

## 🚀 Ejecución en desarrollo

```bash
# Activar entorno virtual
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS

# Ejecutar servidor de desarrollo
python manage.py runserver
```

### URLs principales

| URL | Descripción |
|---|---|
| `/` | Página principal (catálogo) |
| `/productos/` | Listado de productos con filtros |
| `/producto/<slug>/` | Detalle público de producto |
| `/cotizar/` | Cotizador rápido (carrito) |
| `/users/login/` | Inicio de sesión |
| `/admin/` | Panel de administración Django |
| `/users/dashboard/` | Dashboard (Admin/Ventas) |

---

## 🌱 Población de datos de prueba

El proyecto incluye scripts para poblar la base de datos con datos de ejemplo:

```bash
# 1. Crear categorías, marcas, productos y usuarios de prueba
python fixtures/seed_data.py

# 2. Asignar imágenes a productos (requiere imágenes en media/products/)
python fixtures/assign_images.py

# 3. Desactivar productos sin imagen
python fixtures/deactivate_no_image.py
```

### Usuarios de prueba

| Rol | Email | Contraseña |
|---|---|---|
| Administrador | admin@admin.com | admin123 |
| Ventas | ventas@ventas.com | ventas123 |
| Cliente | cliente@cliente.com | cliente123 |

---

## 🌍 Despliegue en producción

### Configuración

```env
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
SECRET_KEY=clave-secreta-muy-larga-y-segura
```

### Recursos estáticos

```bash
python manage.py collectstatic
```

### Servidor WSGI (Gunicorn)

```bash
pip install gunicorn
gunicorn catalogo2026.wsgi:application --bind 0.0.0.0:8000
```

### Proxy reverso (Nginx)

```nginx
server {
    listen 80;
    server_name tudominio.com;

    location /static/ {
        alias /ruta/al/proyecto/staticfiles/;
    }

    location /media/ {
        alias /ruta/al/proyecto/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### Base de datos (PostgreSQL en producción)

- Usar PostgreSQL 14+ con conexiones SSL
- Configurar backups automáticos con `pg_dump`
- Recomendado: **pgBouncer** para connection pooling

### Variables de entorno en producción

- Configurar `DEBUG=False`
- Generar una `SECRET_KEY` segura: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Usar `ALLOWED_HOSTS` con los dominios exactos
- Configurar las credenciales de SMTP con una [App Password de Google](https://support.google.com/accounts/answer/185833)

---

## 🏗 Arquitectura

### Jerarquía de herencia de templates

```
base.html
├── home/base_home.html         → Portal público (header + footer)
├── products/base_products.html → Administración de productos
└── users/base_users.html       → Autenticación
    └── users/base_panel.html   → Layout de panel (sidebar + contenido)
        ├── dashboard.html
        ├── perfil.html
        ├── lista_usuarios.html
        └── ...
```

### Permisos por rol

| Funcionalidad | Admin | Ventas | Cliente |
|---|:---:|:---:|:---:|
| Ver catálogo público | ✅ | ✅ | ✅ |
| Enviar cotización | ✅ | ✅ | ✅ |
| Dashboard | ✅ | ✅ | ❌ |
| Movimientos de inventario | ✅ | ✅ | ❌ |
| Ver cotizaciones | ✅ | ❌ | ❌ |
| Gestionar productos | ✅ | ❌ | ❌ |
| Gestionar usuarios | ✅ | ❌ | ❌ |

### API Endpoints

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/productos/` | GET | Búsqueda AJAX de productos |
| `/api/productos/filtrar/` | GET | Filtrado por categoría/marca |
| `/cotizacion/cart/toggle/<id>/` | POST | Agregar/quitar producto del carrito |

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.

```
MIT License

Copyright (c) 2026 Solutions Mech Perú

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">Desarrollado con ❤️ por <a href="#">Solutions Mech Perú</a> — 2026</p>
