from django.conf import settings
from django.db.models import Count, Q
from applications.products.models import Category

def whatsapp_number(request):
    return {'whatsapp_number': settings.WHATSAPP_NUMBER}

def categories_processor(request):
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    ).order_by('name')
    return {'nav_categories': categories}

def cart_count_processor(request):
    cart = request.session.get('quotation_cart', {})
    return {'header_cart_count': sum(cart.values())}
