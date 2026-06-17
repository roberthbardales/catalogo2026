from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models, transaction
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from applications.users.mixins import AdministradorPermisoMixin

from .forms import (
    BrandForm,
    CategoryForm,
    ProductForm,
    ProductImageFormSet,
    TechnicalSpecificationFormSet,
)
from applications.inventory.models import StockMovement

from .models import Brand, Category, Product


class ProductListView(AdministradorPermisoMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        qs = Product.objects.select_related('category', 'brand').prefetch_related('tags').order_by('name')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                models.Q(name__icontains=q)
                | models.Q(sku__icontains=q)
                | models.Q(short_description__icontains=q)
                | models.Q(description__icontains=q)
                | models.Q(category__name__icontains=q)
                | models.Q(brand__name__icontains=q)
            )
        category_id = self.request.GET.get('category', '').strip()
        if category_id and category_id.isdigit():
            qs = qs.filter(category_id=int(category_id))
        brand_id = self.request.GET.get('brand', '').strip()
        if brand_id and brand_id.isdigit():
            qs = qs.filter(brand_id=int(brand_id))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['categories'] = Category.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=models.Q(products__is_active=True))
        ).order_by('name')
        ctx['brands'] = Brand.objects.filter(is_active=True).order_by('name')
        ctx['current_category'] = self.request.GET.get('category', '')
        ctx['current_brand'] = self.request.GET.get('brand', '')
        return ctx


class ProductDetailView(AdministradorPermisoMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self):
        return super().get_queryset().select_related('category', 'brand').prefetch_related(
            'images', 'specifications',
        ).get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recent_movements'] = StockMovement.objects.filter(
            product=self.object
        ).select_related('created_by').order_by('-created')[:10]
        return ctx


class ProductCreateView(AdministradorPermisoMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('app_products:product-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_formset'] = ProductImageFormSet()
        ctx['spec_formset'] = TechnicalSpecificationFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        image_formset = ProductImageFormSet(self.request.POST, self.request.FILES)
        spec_formset = TechnicalSpecificationFormSet(self.request.POST, self.request.FILES)
        if not image_formset.is_valid() or not spec_formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form, image_formset=image_formset, spec_formset=spec_formset))
        with transaction.atomic():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            spec_formset.instance = self.object
            spec_formset.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        ctx = self.get_context_data(
            form=form,
            image_formset=ProductImageFormSet(self.request.POST, self.request.FILES),
            spec_formset=TechnicalSpecificationFormSet(self.request.POST, self.request.FILES),
        )
        return self.render_to_response(ctx)


class ProductUpdateView(AdministradorPermisoMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('app_products:product-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_formset'] = ProductImageFormSet(instance=self.object)
        ctx['spec_formset'] = TechnicalSpecificationFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        image_formset = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        spec_formset = TechnicalSpecificationFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if not image_formset.is_valid() or not spec_formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form, image_formset=image_formset, spec_formset=spec_formset))
        with transaction.atomic():
            self.object = form.save()
            image_formset.save()
            spec_formset.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        ctx = self.get_context_data(
            form=form,
            image_formset=ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object),
            spec_formset=TechnicalSpecificationFormSet(self.request.POST, self.request.FILES, instance=self.object),
        )
        return self.render_to_response(ctx)


class ProductDeleteView(AdministradorPermisoMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('app_products:product-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class CategoryListView(AdministradorPermisoMixin, ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        return Category.objects.order_by('name')


class CategoryCreateView(AdministradorPermisoMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('app_products:category-list')


class CategoryUpdateView(AdministradorPermisoMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('app_products:category-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class CategoryDeleteView(AdministradorPermisoMixin, DeleteView):
    model = Category
    template_name = 'products/category_confirm_delete.html'
    success_url = reverse_lazy('app_products:category-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class BrandListView(AdministradorPermisoMixin, ListView):
    model = Brand
    template_name = 'products/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10

    def get_queryset(self):
        return Brand.objects.order_by('name')


class BrandCreateView(AdministradorPermisoMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('app_products:brand-list')


class BrandUpdateView(AdministradorPermisoMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('app_products:brand-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class BrandDeleteView(AdministradorPermisoMixin, DeleteView):
    model = Brand
    template_name = 'products/brand_confirm_delete.html'
    success_url = reverse_lazy('app_products:brand-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
