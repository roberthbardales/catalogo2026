from django.urls import path

from . import views

app_name = 'app_products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('crear/', views.ProductCreateView.as_view(), name='product-create'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/editar/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<slug:slug>/eliminar/', views.ProductDeleteView.as_view(), name='product-delete'),
]
