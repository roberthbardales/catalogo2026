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
        ).select_related('category', 'brand')[:6]
        ctx['categories'] = Category.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')[:6]
        ctx['on_sale_products'] = Product.objects.filter(
            is_active=True, sale_price__isnull=False
        ).select_related('brand')[:10]
        ctx['testimonials'] = [
            {'name': 'Carlos Mendoza', 'role': 'Gerente de TI — Corporación Nova', 'text': 'El proceso de cotización fue rápido y el equipo nos ayudó a elegir los equipos adecuados para nuestra empresa.'},
            {'name': 'María Fernanda López', 'role': 'Administradora — Centro Educativo San José', 'text': 'Comprar 30 laptops para nuestro laboratorio nunca fue tan sencillo. Excelente atención postventa.'},
            {'name': 'Ricardo Gálvez', 'role': 'CEO — TechSolutions EIRL', 'text': 'Trabajamos con ellos desde 2024 y siempre cumplen los plazos. Los precios corporativos son muy competitivos.'},
        ]
        ctx['brands'] = Brand.objects.filter(is_active=True).order_by('name')
        return ctx


class AboutView(TemplateView):
    template_name = 'home/about.html'


class ProductsView(ListView):
    model = Product
    template_name = 'home/products.html'
    context_object_name = 'products'
    paginate_by = 15

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
        brand_id = self.request.GET.get('brand', '').strip()
        if brand_id and brand_id.isdigit():
            qs = qs.filter(brand_id=int(brand_id))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['categories'] = Category.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        ctx['brands'] = Brand.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        ctx['current_category'] = self.request.GET.get('category', '')
        ctx['current_brand'] = self.request.GET.get('brand', '')
        return ctx


class CategoriesView(TemplateView):
    template_name = 'home/categories.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        return ctx


class BrandsView(TemplateView):
    template_name = 'home/brands.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['brands'] = Brand.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        return ctx


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
