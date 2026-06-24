from django.urls import path

from . import views

app_name = 'app_home'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('nosotros/', views.AboutView.as_view(), name='about'),
    path('productos/', views.ProductsView.as_view(), name='products'),
    path('categorias/', views.CategoriesView.as_view(), name='categories'),
    path('marcas/', views.BrandsView.as_view(), name='brands'),
    path('garantia/', views.WarrantyView.as_view(), name='warranty'),
    path('contacto/', views.ContactView.as_view(), name='contact'),
    path('api/productos/', views.ProductSearchAPIView.as_view(), name='product-search-api'),
    path('api/productos/filtrar/', views.ProductFilterAPIView.as_view(), name='product-filter-api'),
]
