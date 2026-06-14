from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from applications.users.mixins import AdministradorPermisoMixin

from .forms import ProductForm
from .models import Product


class ProductListView(AdministradorPermisoMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.select_related('category', 'brand').prefetch_related('tags').order_by('name')


class ProductDetailView(AdministradorPermisoMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class ProductCreateView(AdministradorPermisoMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('app_products:product-list')


class ProductUpdateView(AdministradorPermisoMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('app_products:product-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class ProductDeleteView(AdministradorPermisoMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('app_products:product-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
