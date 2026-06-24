from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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


def _parse_id_list(raw):
    if not raw:
        return []
    return [int(x) for x in raw.split(',') if x.strip().isdigit()]


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
        cat_ids = _parse_id_list(self.request.GET.get('categories', ''))
        if cat_ids:
            qs = qs.filter(category_id__in=cat_ids)
        brd_ids = _parse_id_list(self.request.GET.get('brands', ''))
        if brd_ids:
            qs = qs.filter(brand_id__in=brd_ids)
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

        raw_cats = self.request.GET.get('categories', '')
        ctx['selected_categories'] = [s.strip() for s in raw_cats.split(',') if s.strip().isdigit()]
        raw_brands = self.request.GET.get('brands', '')
        ctx['selected_brands'] = [s.strip() for s in raw_brands.split(',') if s.strip().isdigit()]
        return ctx


class ProductFilterAPIView(View):
    def get(self, request):
        qs = Product.objects.filter(is_active=True).select_related('category', 'brand')

        q = request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(short_description__icontains=q)
                | Q(category__name__icontains=q)
                | Q(brand__name__icontains=q)
            )

        cat_ids = _parse_id_list(request.GET.get('categories', ''))
        if cat_ids:
            qs = qs.filter(category_id__in=cat_ids)

        brd_ids = _parse_id_list(request.GET.get('brands', ''))
        if brd_ids:
            qs = qs.filter(brand_id__in=brd_ids)

        paginator = Paginator(qs, 15)
        page = request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        products_data = []
        for p in page_obj.object_list:
            products_data.append({
                'id': p.id,
                'name': p.name,
                'slug': p.slug,
                'sku': p.sku,
                'price': str(p.price),
                'sale_price': str(p.sale_price) if p.sale_price else None,
                'effective_price': str(p.effective_price),
                'on_sale': p.on_sale,
                'stock': p.stock,
                'image_main': p.image_main.url if p.image_main else '',
                'brand_name': p.brand.name,
                'category_name': p.category.name,
            })

        return JsonResponse({
            'products': products_data,
            'page': page_obj.number,
            'num_pages': paginator.num_pages,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'total': paginator.count,
        })


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
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        ctx['brands'] = Brand.objects.filter(is_active=True).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        return ctx


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
