# Proyecto: Catálogo 2026 — Estado al 17/06/2026

## Estructura de templates

```
templates/
├── base.html                        # Base raíz (sin header/footer, solo bloques)
│   ├── home/base_home.html          # Hereda base.html, agrega header/footer
│   ├── products/base_products.html  # Hereda base.html, agrega header/footer
│   └── users/
│       ├── base_users.html          # Hereda base.html, agrega header/footer
│       └── base_panel.html          # Hereda base_users, layout sidebar + content
├── include/
│   ├── header.html
│   ├── footer.html
│   └── panel_sidebar.html           # Sidebar reutilizable (Perfil, Productos)
├── home/       → heredan de home/base_home.html
├── products/   → heredan de products/base_products.html
└── users/
    ├── base_users.html
    ├── base_panel.html
    ├── login.html                   → hereda base_users (sin panel)
    ├── register.html                → hereda base_users (sin panel)
    ├── perfil.html                  → hereda base_panel, usa panel_content
    ├── cambiar_password.html        → hereda base_panel, usa panel_content
    ├── lista_usuarios.html          → hereda base_panel, usa panel_content
    └── editar_usuario.html          → hereda base_panel, usa panel_content
```

## Jerarquía de herencia

```
base.html  (header/footer blocks vacíos)
├── home/base_home.html     → rellena header/footer blocks
├── products/base_products.html → rellena header/footer blocks
└── users/base_users.html   → rellena header/footer blocks
    └── users/base_panel.html  → layout row (sidebar 3 + content 9)
        ├── perfil.html          → panel_content (secciones: perfil, usuarios)
        ├── cambiar_password.html → panel_content (formulario)
        ├── lista_usuarios.html  → panel_content (tabla)
        └── editar_usuario.html  → panel_content (formulario)
```

## Sidebar del panel (panel_sidebar.html)

- **Perfil** (siempre visible) — activo cuando `url_name == 'perfil'` y `section != 'products'`
- **Productos** (solo admin: `is_superuser` u `occupation == '0'`) — activo cuando `section == 'products'`
- **Inicio** → `app_home:index`
- **Salir** → `app_users:logout`

El ítem activo se detecta automáticamente vía `request.resolver_match.url_name` y `request.GET.section`.

## Perfil (perfil.html)

- Sección por defecto: `perfil` (información del usuario)
- Sección `usuarios`: listado de usuarios (solo admin)
- Dentro de `perfil`: botones para "Cambiar Contraseña" y "Lista Usuarios" (solo admin)

## Seed de productos

- **Management command**: `applications/products/management/commands/seed_products.py`
  - Crea 10 categorías (Laptops, Audífonos, Periféricos, etc.)
  - Crea 10 marcas reales (Samsung, Apple, Sony, LG, Dell, HP, Lenovo, ASUS, Microsoft, Logitech)
  - Crea 100 productos (10 por categoría) sin imágenes, con precio y stock aleatorios
  - **Idempotente**: omite SKUs existentes, seguro de ejecutar múltiples veces
  - Uso: `python manage.py seed_products`
- **Fixture JSON**: `fixtures/seed_productos.json`
  - 120 objetos (10 cat + 10 marcas + 100 productos)
  - Uso: `python manage.py loaddata seed_productos`

## Paginación

- `ProductListView` usa `paginate_by = 10`
- Controles de paginación Bootstrap en `templates/products/product_list.html`
  - Botones: Primero, Anterior, números (±3), Siguiente, Último
  - Preserva `?q=` al navegar entre páginas

## Últimos cambios

### 17/06/2026 — Footer rediseñado + sidebar categorías + buscador en header + hover cards
- Rediseñado `templates/include/footer.html`: estructura 4 columnas (descripción, enlaces, contacto, sígueme) sin estilos inline ni clases de color
- Agregado sidebar de categorías en `templates/products/product_list.html` (panel admin) con `product_count` vía `annotate` en `ProductListView`
- Convertido `ProductsView` (vista pública `/productos/`) de `TemplateView` a `ListView` con paginación (12), filtro por categoría y búsqueda
- Agregado sidebar de categorías en `templates/home/products.html` con buscador, grid de productos y paginación
- Creado `static/css/product-card.css` con efecto hover: `translateY(-4px)`, sombra elevada, borde primary
- Al hacer hover sobre la card, el nombre del producto se colorea con `--bs-primary`
- Imagen y nombre del producto ahora linkean a `public-product-detail` (antes solo botón Cotizar)
- Badge de categoría reemplazado por marca, y marca abajo reemplazada por categoría
- Movido buscador AJAX de `templates/home/index.html` a `templates/include/header.html` (dentro del navbar, al costado de "Catálogo 2026", visible solo en desktop)
- Acercados horizontalmente los links de navegación (`gap-lg-1`, `px-lg-2`)

### 14/06/2026 — Seed de productos con marcas reales + paginación
- Creado `applications/products/management/commands/seed_products.py`
- Creado `fixtures/seed_productos.json` con dump de categorías, marcas y 100 productos
- Agregada paginación Bootstrap a `templates/products/product_list.html`
- Marcas actualizadas a nombres reales (Samsung, Apple, Sony, etc.)

### 14/06/2026 — Renombrado ruta y clase dashboard → perfil
- `name='dashboard'` renombrado a `name='perfil'` en `urls.py`
- `DashboardView` renombrado a `PerfilView` en `views.py`
- `settings.py`, `reverse_lazy` y templates actualizados para usar `app_users:perfil`
- Texto "Dashboard" en header cambiado a "Perfil"

### 13/06/2026 — Sidebar simplificado
Sidebar simplificado a solo 2 opciones: Perfil y Productos. Dentro de Perfil están los botones a Cambiar Contraseña y Usuarios.

### 14/06/2026 — Renombrado dashboard → perfil, productos movidos a /products/
- `dashboard.html` renombrado a `perfil.html` y su estilo unificado con el patrón de `product_list.html` (header `d-flex`, contenido en `card shadow-sm border-0`)
- Productos eliminados del panel (`?section=products` ya no existe en perfil.html)
- Sidebar de Productos ahora apunta directamente a `app_products:product-list` (`/products/`)
- Sidebar simplificado: removida variable `section` del `{% with %}`

### 14/06/2026 — Módulo Inventory completo (CRUD de movimientos de stock)
- Creado `applications/inventory/forms.py` — `StockMovementForm` con validación de stock insuficiente para OUT
- Creado `applications/inventory/signals.py` — `post_save` en `StockMovement` actualiza `Product.stock` automáticamente
- Creado `applications/inventory/urls.py` — 2 rutas: `movement-list` (`/inventory/`) y `movement-create` (`/inventory/crear/`)
- Actualizado `applications/inventory/views.py` — `MovementListView` (paginado, busca por q, filtro por tipo) y `MovementCreateView` (asigna `created_by` automáticamente). Permiso: `VentasPermisoMixin` (Admin + Ventas)
- Actualizado `applications/inventory/apps.py` — importa signals en `ready()`
- Actualizado `catalogo2026/urls.py` — incluye `applications.inventory.urls`
- Creado `templates/inventory/movement_list.html` — tabla con búsqueda, filtro por tipo, paginación
- Creado `templates/inventory/movement_form.html` — formulario con select de producto + tipo + cantidad + nota
- Actualizado `templates/include/panel_sidebar.html` — link "Movimientos" visible para Admin + Ventas (antes solo para Admin)
- Actualizado `templates/products/product_detail.html` y `ProductDetailView` — sección "Últimos movimientos de stock" (últimos 10)

### 14/06/2026 — Filtros por categoría y marca en listado de productos
- Actualizado `applications/products/views.py` — `ProductListView` ahora filtra por `?category=<id>` y `?brand=<id>`, pasa `categories`, `brands`, `current_category`, `current_brand` al template
- Actualizado `templates/products/product_list.html` — formulario en fila con buscador + select categoría + select marca + botón limpiar. Paginación preserva `q`, `category` y `brand`

### 15/06/2026 — Fix: Cannot filter a query once a slice has been taken
- Bug: `Prefetch('stock_movements', queryset=StockMovement.objects...[:10])` en `ProductDetailView.get_object` causaba error porque Django intenta filtrar el queryset prefetch (ya sliceado) con `product_id__in=()`
- Fix: Movido a `get_context_data` — primero se filtra por `product=self.object`, luego se aplica `[:10]`
- Actualizado template `product_detail.html`: `product.stock_movements.all` → `recent_movements`

### 14/06/2026 — Buscador AJAX en tiempo real en home
- Actualizado `applications/home/views.py` — nueva `ProductSearchAPIView` (endpoint JSON, busca por `name__icontains`, límite 10, retorna id/name/slug/price/stock/category/brand)
- Actualizado `applications/home/urls.py` — nueva ruta `api/productos/` → `product-search-api`
- Actualizado `templates/home/index.html` — input de búsqueda en la parte superior, resultados en tiempo real (sin debounce, sin mínimo de caracteres) con Fetch API, muestra nombre, categoría, marca, precio y stock

### 15/06/2026 — Módulo de Cotizaciones + Productos públicos
- Creada app `applications.quotations`:
  - **Modelos**: `QuotationRequest` (nombre, email, teléfono, notas, estado) y `QuotationItem` (producto, cantidad, precio snapshot, subtotal)
  - **Vistas públicas**: `PublicProductDetailView` (detalle + formulario cotizar), `CreateQuotationView` (POST, crea solicitud), `QuotationThanksView` (confirmación)
  - **Vistas admin**: `QuotationListView` (listado paginado con filtro por estado), `QuotationDetailView` (detalle + cambiar estado), `QuotationStatusUpdateView` (POST)
  - **Rutas públicas**: `/cotizacion/<slug:slug>/`, `/cotizacion/crear/`, `/cotizacion/gracias/`
  - **Rutas admin**: `/cotizaciones/`, `/cotizaciones/<int:pk>/`, `/cotizaciones/<int:pk>/estado/`
  - Templates: `public_product_detail.html`, `thanks.html`, `quotation_list.html`, `quotation_detail.html`
- Actualizado `templates/home/products.html` — ahora lista productos reales desde BD con link a cotización
- Actualizado `templates/include/panel_sidebar.html` — nuevo ítem "Cotizaciones" (solo admin)
- Actualizado `catalogo2026/settings.py` → `applications.quotations` en INSTALLED_APPS

### 15/06/2026 — Unificada ruta de imágenes + miniatura en buscador AJAX
- Unificados `upload_to` de `Product.image_main` y `ProductImage.image` a `products/` (antes `products/main/` y `products/gallery/`)
- Movidas 18 imágenes de `media/` a `media/products/`
- Creado `assign_product_images.py` — asigna las 18 imágenes a los primeros 18 productos sin imagen
- Actualizado `fixtures/seed_productos.json` con `dumpdata` (incluye `image_main` en 19 productos)
- Desactivados 81 productos sin imagen (`is_active=False`)
- Agregada miniatura (50x50px) en resultados del buscador AJAX del home (`ProductSearchAPIView` + `index.html`)
- Mejorado `home/products.html`: imágenes con `object-fit: contain` y `max-height: 180px` para evitar recorte vertical
- Rediseñado `home/index.html`: hero comercial, stats dinámicos desde BD, productos destacados, categorías, cards de beneficios
- Resultados del buscador AJAX ahora son links clickeables al detalle del producto
