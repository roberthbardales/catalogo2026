from django.urls import path

from . import views

app_name = 'app_quotations'

urlpatterns = [
    # Públicas
    path('cotizacion/<slug:slug>/', views.PublicProductDetailView.as_view(), name='public-product-detail'),
    path('cotizacion/crear/', views.CreateQuotationView.as_view(), name='quotation-create'),
    path('cotizacion/gracias/', views.QuotationThanksView.as_view(), name='quotation-thanks'),

    # Admin
    path('cotizaciones/', views.QuotationListView.as_view(), name='quotation-list'),
    path('cotizaciones/<int:pk>/', views.QuotationDetailView.as_view(), name='quotation-detail'),
    path('cotizaciones/<int:pk>/estado/', views.QuotationStatusUpdateView.as_view(), name='quotation-update-status'),
]
