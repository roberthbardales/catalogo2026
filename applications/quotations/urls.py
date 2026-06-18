from django.urls import path

from . import views

app_name = 'app_quotations'

urlpatterns = [
    # Cotizador rápido (carrito en sesión)
    path('cotizar/', views.QuotationBuildView.as_view(), name='quotation-build'),
    path('cotizacion/cart/toggle/<int:pk>/', views.QuotationCartToggleView.as_view(), name='cart-toggle'),
    path('cotizacion/enviar/', views.QuotationCreateFromCartView.as_view(), name='quotation-create-from-cart'),

    # Públicas (individual) — rutas fijas ANTES de <slug>
    path('cotizacion/crear/', views.CreateQuotationView.as_view(), name='quotation-create'),
    path('cotizacion/<slug:slug>/', views.PublicProductDetailView.as_view(), name='public-product-detail'),

    # Admin
    path('cotizaciones/', views.QuotationListView.as_view(), name='quotation-list'),
    path('cotizaciones/<int:pk>/', views.QuotationDetailView.as_view(), name='quotation-detail'),

]
