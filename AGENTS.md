# Proyecto: Catálogo 2026 — Estado al 13/06/2026

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
    ├── dashboard.html               → hereda base_panel, usa panel_content
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
        ├── dashboard.html       → panel_content (secciones: perfil, productos)
        ├── cambiar_password.html → panel_content (formulario)
        ├── lista_usuarios.html  → panel_content (tabla)
        └── editar_usuario.html  → panel_content (formulario)
```

## Sidebar del panel (panel_sidebar.html)

- **Perfil** (siempre visible) — activo cuando `url_name == 'dashboard'` y `section != 'products'`
- **Productos** (solo admin: `is_superuser` u `occupation == '0'`) — activo cuando `section == 'products'`
- **Inicio** → `app_home:index`
- **Salir** → `app_users:logout`

El ítem activo se detecta automáticamente vía `request.resolver_match.url_name` y `request.GET.section`.

## Dashboard (dashboard.html)

- Sección por defecto: `perfil` (información del usuario)
- Sección `products`: tabla CRUD de productos (solo admin)
- Dentro de `perfil`: botones para "Cambiar Contraseña" y "Lista Usuarios" (solo admin)

## Último cambio del día 13/06/2026

Sidebar simplificado a solo 2 opciones: Perfil y Productos. Dentro de Perfil están los botones a Cambiar Contraseña y Usuarios.
