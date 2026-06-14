from django.urls import path

from . import views

app_name = 'app_products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('crear/', views.ProductCreateView.as_view(), name='product-create'),
    # Categorías (deben ir antes de <slug> para evitar conflictos)
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/crear/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<slug:slug>/editar/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<slug:slug>/eliminar/', views.CategoryDeleteView.as_view(), name='category-delete'),
    # Marcas (deben ir antes de <slug> para evitar conflictos)
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('brands/crear/', views.BrandCreateView.as_view(), name='brand-create'),
    path('brands/<slug:slug>/editar/', views.BrandUpdateView.as_view(), name='brand-update'),
    path('brands/<slug:slug>/eliminar/', views.BrandDeleteView.as_view(), name='brand-delete'),
    # Productos (slugs comodín van al final)
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/editar/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<slug:slug>/eliminar/', views.ProductDeleteView.as_view(), name='product-delete'),
]
