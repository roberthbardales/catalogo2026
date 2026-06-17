from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.generic import ListView, TemplateView, View

from applications.products.models import Brand, Category, Product


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_products'] = Product.objects.filter(is_active=True).count()
        ctx['total_categories'] = Category.objects.filter(is_active=True).count()
        ctx['total_brands'] = Brand.objects.filter(is_active=True).count()
        ctx['featured_products'] = Product.objects.filter(
            is_active=True
        ).select_related('category', 'brand')[:4]
        ctx['categories'] = Category.objects.filter(is_active=True)[:6]
        return ctx


class AboutView(TemplateView):
    template_name = 'home/about.html'


class ProductsView(ListView):
    model = Product
    template_name = 'home/products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category', 'brand')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(short_description__icontains=q)
                | Q(category__name__icontains=q)
                | Q(brand__name__icontains=q)
            )
        category_id = self.request.GET.get('category', '').strip()
        if category_id and category_id.isdigit():
            qs = qs.filter(category_id=int(category_id))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['categories'] = Category.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        ctx['current_category'] = self.request.GET.get('category', '')
        return ctx


class CategoriesView(TemplateView):
    template_name = 'home/categories.html'


class BrandsView(TemplateView):
    template_name = 'home/brands.html'


class WarrantyView(TemplateView):
    template_name = 'home/warranty.html'


class ContactView(TemplateView):
    template_name = 'home/contact.html'


class ProductSearchAPIView(View):
    def get(self, request):
        q = request.GET.get('q', '').strip()
        if not q or len(q) < 2:
            return JsonResponse({'results': []})
        products = Product.objects.filter(
            is_active=True,
            name__icontains=q,
        ).select_related('category', 'brand')[:10]
        results = [
            {
                'id': p.id,
                'name': p.name,
                'slug': p.slug,
                'price': str(p.price),
                'stock': p.stock,
                'image_main': p.image_main.url if p.image_main else '',
                'category': p.category.name,
                'brand': p.brand.name,
            }
            for p in products
        ]
        return JsonResponse({'results': results})
