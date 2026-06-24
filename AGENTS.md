# Proyecto: Catálogo 2026 — Estado al 22/06/2026

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
│   ├── header.html                  # Announcement bar + navbar con search AJAX
│   ├── footer.html
│   └── panel_sidebar.html           # Sidebar reutilizable (Dashboard, Perfil, Productos)
├── home/       → heredan de home/base_home.html
├── products/   → heredan de products/base_products.html
└── users/
    ├── base_users.html
    ├── base_panel.html
    ├── login.html                   → hereda base_users (sin panel)
    ├── register.html                → hereda base_users (sin panel)
    ├── perfil.html                  → hereda base_panel, usa panel_content
    ├── dashboard.html               → hereda base_panel, usa panel_content
    ├── cambiar_password.html        → hereda base_panel, usa panel_content (solo admin)
    ├── lista_usuarios.html          → hereda base_panel, usa panel_content
    ├── editar_usuario.html          → hereda base_panel, usa panel_content
    └── reset_password.html          → hereda base_panel, usa panel_content (solo admin)
```

## Jerarquía de herencia

```
base.html  (header/footer blocks vacíos)
├── home/base_home.html     → rellena header/footer blocks
├── products/base_products.html → rellena header/footer blocks
└── users/base_users.html   → rellena header/footer blocks
    └── users/base_panel.html  → layout row (sidebar 2 + content 10)
        ├── perfil.html          → panel_content (secciones: perfil, usuarios)
        ├── dashboard.html       → panel_content (KPIs, cotizaciones recientes, stock bajo)
        ├── cambiar_password.html → panel_content (formulario)
        ├── lista_usuarios.html  → panel_content (tabla)
        └── editar_usuario.html  → panel_content (formulario)
```

## Sidebar del panel (panel_sidebar.html)

- **Perfil** (siempre visible) — activo cuando `url_name == 'perfil'` y `section != 'products'`
- **Dashboard** (Admin + Ventas) — activo cuando `url_name == 'dashboard'`
- **Movimientos** (Admin + Ventas)
- **Cotizaciones** (solo admin)
- **Productos**, **Categorías**, **Marcas** (solo admin)
- **Inicio** → `app_home:index`
- **Salir** → `app_users:logout`

El ítem activo se detecta automáticamente vía `request.resolver_match.url_name`.

## Perfil (perfil.html)

- Sección por defecto: `perfil` (información del usuario)
- Sección `usuarios`: listado de usuarios (solo admin)
- Dentro de `perfil`: botones para "Cambiar Contraseña" y "Lista Usuarios" (solo admin)

## Dashboard (dashboard.html)

- **Ruta**: `/users/dashboard/` — nombre `app_users:dashboard`
- **Vista**: `DashboardView` (VentasPermisoMixin — Admin + Ventas)
- **KPIs**: Productos activos, Categorías, Marcas, Cotizaciones, Stock bajo, Sin stock
- **Tablas**: Últimas 5 cotizaciones + Productos con stock bajo (&lt;5)

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

## Precio de oferta (sale_price)

- Modelo `Product` tiene campo `sale_price` (opcional, `DecimalField`)
- Propiedad `on_sale`: `True` si `sale_price` tiene valor
- Propiedad `effective_price`: retorna `sale_price` si existe, sino `price`
- Se usa en cotizaciones (email), carrito, cards y detalle de producto
- Se configura desde el formulario de edición (`product_form.html`) y admin

## Últimos cambios

### 24/06/2026 — Header: btn-outline-teal, carrito con badge, toast notificación
- **Header** (`templates/include/header.html`):
  - Botón "Categorías" cambiado de `btn-outline-primary` a `btn-outline-teal` (clase CSS personalizada con `#0f766e`)
  - Hover de dropdown items más visible: `background-color: rgba(15, 118, 110, 0.1)` + texto `#0f766e`
  - Agregado link "Cotizar" en el nav con badge rojo (`cart-badge`) que muestra cantidad de productos en carrito
  - Badge posición ajustada (`top:8px` en vez de `top-0`)
  - Animación shake en el badge al agregar producto (`@keyframes cart-badge-shake`)
  - Agregado **Toast Bootstrap** autodescartable (4s) al agregar producto: "Producto agregado a cotización" + botones [Seguir] e [Ir al carrito]
  - Agregada clase `.btn-teal` (fondo sólido `#0f766e`) para el botón "Ir al carrito"
  - Función global `window.showAddToast()` y `window.updateCartBadge(count)`
- **Context processor** (`applications/procesors.py`): nuevo `cart_count_processor` que expone `header_cart_count` (suma de cantidades del carrito en sesión)
- **Settings** (`catalogo2026/settings.py`): registrado `cart_count_processor`
- **Products** (`templates/home/products.html`): `bindAddToCart` ahora llama `showAddToast()` al agregar
- **Index** (`templates/home/index.html`): mismo cambio en el JS de "Agregar"

### 23/06/2026 — Sidebar productos: tabs → accordion, header fixes
- **Sidebar productos** (`templates/home/products.html`): tabs de Marcas/Categorías reemplazadas por accordion Bootstrap
  - Categorías primero (expandido por defecto), Marcas después (colapsado)
  - JS que previene colapsar una sección si tiene checkboxes marcados
- **Header** (`templates/include/header.html`):
  - Eliminado badge `product_count` del dropdown de categorías
  - Fix: `?category=` → `?categories=` (el link dejó de funcionar al cambiar el view a plural)
  - Buscador AJAX simplificado: solo imagen, nombre y precio (sin descripción ni stock)
  - Input de búsqueda más ancho: 400px → 600px

### 22/06/2026 — Plan: Filtro productos con accordion Marcas→Categorías / Categorías→Marcas

- Sidebar de productos (`home/products.html`) actualmente: dos pestañas (Marcas / Categorías) con flat lists de checkboxes que hacen fetch AJAX a `/api/productos/filtrar/`
- **Plan**: Convertir cada pestaña en un accordion donde cada marca expande sus categorías y cada categoría expande sus marcas
- **Backend**: Agregar `brand_categories` (brand_id → {name, categories[]}) y `category_brands` (category_id → {name, brands[]}) al contexto de `ProductsView`
  - Ambos se construyen desde `Product.objects.values('brand_id', 'brand__name', 'category_id', 'category__name').distinct()`
- **Frontend**: Marcas tab → accordion con checkbox en header + categories como sub-items colapsables. Categorías tab → mismo patrón al revés
- **Pendiente**: definir si check de sub-opción envía solo su tipo o ambos (marca + categoría)
- Decidido: guardar plan en AGENTS.md y abandonar la implementación por ahora

### 22/06/2026 — Spacing unificado en index.html (todo a -2), fixes franja de ofertas, logos marcas más grandes
- `templates/home/index.html`: unificados todos los valores de margin, padding y gap a `-2` (0.5rem)
  - `mb-0/1/3/4` → `mb-2`, `mt-1/4` → `mt-2`, `me-1` → `me-2`
  - `p-3/4/5` → `p-2`, `py-0/1/5` → `py-2`, `px-4` → `px-2`
  - `gap-1/3` → `gap-2`, `g-0/3/4` → `g-2`
  - Total ~70 ocurrencias actualizadas
- `templates/home/products.html`: intento similar revertido a estado original
- **Franja de ofertas**: eliminado `@keyframes scroll-offers` muerto, eliminado `gap: 1rem` del CSS `.offer-track` (usaba `gap-2` de Bootstrap), corregido offset JS de 12→16px para coincidir con gap real
- **Marcas**: logos aumentados de 32×32 a 48×48; padding horizontal de cards reducido (`p-2` → `py-2 px-1`)

### 20/06/2026 — Registro solo admin, app notifications (creada y revertida)
- `UserRegisterView` restringido solo a admin vía `AdministradorPermisoMixin`; `success_url` cambiado a `app_users:user-list`
- Creada app `applications/notifications` con modelo `Notification`, señales (`StockMovement < 5`, nuevas cotizaciones), campana en header con polling AJAX, y página de listado en el panel — **revertido completamente** poco después

### 20/06/2026 — Logo en header, buscador centrado, botón Categorías con dropdown
- Reemplazado texto "C" + "Catálogo" por `logo.png` en el navbar-brand del header
- Buscador movido a `position-absolute start-50 translate-middle-x` para centrarlo horizontalmente entre logo y toggler (oculto en móvil)
- Creado `categories_processor` en `applications/procesors.py` que inyecta `nav_categories` (categorías activas con `product_count`) en todos los templates vía context processor
- Registrado `categories_processor` en `catalogo2026/settings.py`
- Agregado botón "Categorías" con dropdown Bootstrap entre el logo y el buscador: lista todas las categorías con badge de conteo + link "Todas las categorías" (solo visible en desktop)

### 19/06/2026 — Footer rediseñado, fix templates sin product-card.css
- Footer rediseñado con 4 columnas: (1) Marca + iconos redes sociales (WhatsApp, Facebook, LinkedIn, correo), (2) Enlaces rápidos (Inicio, Productos, Cotización, Contacto), (3) Atención + horarios (Lun–Vie 9–18 / Sáb 9–13), (4) Ubicación + botón "Cotiza por WhatsApp"
- Agregado "↑ Volver arriba" con `scrollTo` smooth en footer-bottom
- CSS footer compactado (`padding: 2.5rem 0 1.25rem`), animaciones hover en links, iconos sociales con círculo y `translateY(-2px)`
- **Fix**: 7 templates públicos que heredan `home/base_home.html` no cargaban `product-card.css`, dejando el footer sin estilos (sin fondo oscuro). Se agregó `{% load static %}` + `{% block extra_css %}` con `product-card.css` en: `contact.html`, `warranty.html`, `categories.html`, `brands.html`, `about.html`, `quotation_build.html`, `public_product_detail.html`

### 19/06/2026 — Gestión de contraseñas solo admin, mejoras UI product_list, detalle público, header compacto
- **Eliminado** password reset público (4 rutas, 6 templates, link en login)
- `UpdatePasswordView` restringido solo a admin (`AdministradorPermisoMixin`)
- Creado `AdminResetPasswordView` para resetear contraseña de cualquier usuario
- Creado `reset_password.html`, `ResetPasswordForm`, botón en `lista_usuarios.html`
- Eliminados campos `new_password`/`confirm_password` de `UserUpdateForm`
- `product_list.html`: filtros categoría/marca/estado, miniaturas 40×40, stock coloreado, badge Oferta, contador, sort por columnas, confirm delete con tooltips, `table-bordered`
- `public_product_detail.html`: breadcrumbs, galería con lightbox, tabs Descripción/Especificaciones, stock bar, total dinámico JS, productos relacionados, card cotización compacto (p-3, inputs sm, botones −/+ sin spinners)
- Header compactado (`py-1`, brand .95rem, nav links `px-lg-1`, botones `btn-sm`)
- Announcement bar agregada (`bg-dark`, dirección centrada, sin link)
- **Buscador unificado**: eliminado form GET duplicado de `products.html`, header search visible en todos los tamaños (quitado `d-none d-lg-block`)
- Sidebar categorías/marcas compactado verticalmente (`py-2 px-3`, títulos `h6 small`, items `py-1 small`)
- Galería de imágenes en detalle: miniaturas ahora en columna vertical a la izquierda de la imagen principal

### 18/06/2026 — Categorías/Marcas dinámicas, Dashboard KPIs, Password reset, Contacto real
- Páginas Categorías y Marcas ahora dinámicas desde BD (`CategoriesView`, `BrandsView` con `get_context_data`)
- Templates `categories.html` y `brands.html` reescritos con `{% for %}` loop, link a filtro de productos
- Agregado filtro por marca (`?brand=id`) en `ProductsView` + sidebar de marcas en `home/products.html`
- Creado `DashboardView` con KPIs (6 cards) + tabla últimas cotizaciones + tabla stock bajo
- Nueva ruta `/users/dashboard/` protegida con `VentasPermisoMixin`
- Agregado ítem "Dashboard" en sidebar (Admin + Ventas)
- `PerfilView` simplificado: solo info del usuario, sin KPIs
- Página Contacto actualizada con datos reales (2 emails, 2 teléfonos, dirección específica)
- Mapa Google ahora apunta a dirección exacta (Av. Esperanza Nro. 616 Int. EL09 – ATE – Lima)
- Descomentados links del header: Categorías, Marcas, Garantía (con detección `active`)
- Agregado flujo completo de recuperación de contraseña (password reset):
  - 4 rutas usando `django.contrib.auth.views`
  - 5 templates: form, done, confirm, complete, email
  - Link "¿Olvidaste tu contraseña?" en login
- Creado `analisis_proyecto.docx` con análisis completo vs requisitos

### 18/06/2026 — sale_price (precio de oferta) + mejoras UI
- Agregado campo `sale_price` al modelo `Product` (DecimalField opcional) con propiedades `on_sale` y `effective_price`
- Migración `0003_product_sale_price` creada y aplicada
- Actualizado `ProductForm` y `product_form.html` para incluir campo "Precio oferta"
- Actualizado `admin.py` para mostrar `sale_price` en `list_display`
- Cards de producto (`home/products.html`): badge "Oferta" rojo superpuesto sobre la imagen, precio original tachado, eliminada categoría
- `home/index.html`: precio de oferta con tachado y badge "Oferta"
- `public_product_detail.html`: precio de oferta en rojo + original tachado
- `quotation_build.html`: carrito usa `effective_price`
- `products/product_list.html` y `products/product_detail.html`: admin muestra `effective_price`
- `QuotationCreateFromCartView` y `CreateQuotationView` envía email con `effective_price` (unit_price, subtotal, total)

### 18/06/2026 — Email SMTP, eliminado status de cotizaciones, modal de confirmación
- Agregada configuración SMTP Gmail en `settings.py` + `.env` para envío de correos
- Eliminado campo `status` de `QuotationRequest` (modelo, vistas, URLs, admin, templates, migración `0002`)
- `QuotationCreateFromCartView` y `CreateQuotationView` ahora envían email con datos del cliente + tabla de productos a `customer_email` y `roberthbardales@gmail.com` (CC)
- Eliminado `/cotizacion/gracias/` (`thanks.html`, `QuotationThanksView`, URL)
- Agregado modal Bootstrap de confirmación al enviar cotización (redirige con `?sent=1` y muestra modal ✅)
- Reemplazado emoji 🔍 por `fa-search` de FontAwesome en el buscador del header
- Reducido margen del breadcrumb en `home/products.html` (`mb-4` → `mb-1`)

### 18/06/2026 — Carrusel hero, footer con datos reales, WhatsApp avanzado, mejoras varias
- Agregado carrusel Bootstrap con 3 slides (Unsplash) al inicio de `home/index.html`, intervalo 3s, overlay oscuro, captions
- Footer actualizado con datos de Solutions Mech Perú: descripción, atención (2 emails + 2 teléfonos), ubicación. Copyright: "© 2026 Solutions Mech Perú · Catálogo 2026"
- Eliminadas secciones Compañía y Enlaces del footer
- Agregado `<hr>` + centrado en footer-bottom
- Agregado FontAwesome 6.5.1 CDN en `base.html` (íconos en footer y WhatsApp ahora visibles)
- Agregados estilos CSS completos para footer en `static/css/product-card.css` (fondo oscuro, tipografía, hover, responsive)
- Arreglado enlace "Cotización" roto en `header.html` (`href=""` → `app_home:products`)
- Agregado debounce (300ms) en buscador AJAX del header para evitar llamadas redundantes
- Creado cotizador rápido con carrito en sesión (`/cotizar/`):
  - `QuotationBuildView` — muestra carrito y formulario de envío
  - `QuotationCartToggleView` — AJAX agrega/remueve productos del carrito en sesión
  - `QuotationCreateFromCartView` — procesa formulario y crea `QuotationRequest` + `QuotationItem` por cada producto
  - `QuotationCartForm` — formulario con nombre, email, teléfono, notas
  - Template `quotations/quotation_build.html` — panel único con lista de productos + formulario
  - Botón "Seguir agregando" linkea a `app_home:products`
- Botón "Agregar" en `home/products.html` ahora hace AJAX POST al carrito de sesión (feedback visual "✓ Agregado" por 2s)
- Botones en cards de `home/products.html`: "Cotizar" (WhatsApp) + "Agregar" (carrito)
- Enlace "Cotización" del header redirigido a `app_quotations:quotation-build`
- WhatsApp por producto: botón verde "Consultar por WhatsApp" en `public_product_detail.html` con nombre + SKU en mensaje
- WhatsApp por producto: icono WhatsApp en cada card de `home/products.html` con nombre del producto
- Rediseñado WhatsApp flotante: tooltip "¿Necesitas ayuda?" al hover, animación pulse, badge "Cotiza aquí" intermitente, popup con 3 opciones (Consultar precio, Soporte técnico, Información general) que se abre al hacer clic
- Actualizada página `home/about.html` con contenido real de Solutions Mech Perú
- Reducido ancho del panel sidebar: `col-lg-3` → `col-lg-2` en `base_panel.html`

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
