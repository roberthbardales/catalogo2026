from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count, Prefetch, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, View

from applications.products.models import Brand, Category, Product
from applications.users.mixins import AdministradorPermisoMixin
from applications.inventory.models import StockMovement

from .forms import PublicQuotationForm, QuotationCartForm
from .models import QuotationItem, QuotationRequest


# =============================================================================
# COTIZADOR RÁPIDO (carrito en sesión)
# =============================================================================

class QuotationBuildView(TemplateView):
    """Página del cotizador: muestra el carrito y formulario de envío"""
    template_name = 'quotations/quotation_build.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = self.request.session.get('quotation_cart', {})
        cart_items = []
        if cart:
            products = Product.objects.filter(
                pk__in=[int(k) for k in cart.keys()], is_active=True
            ).select_related('brand')
            for p in products:
                qty = cart.get(str(p.pk), 0)
                if qty > 0:
                    cart_items.append({
                        'product': p,
                        'quantity': qty,
                        'subtotal': qty * p.effective_price,
                    })
        ctx['cart_items'] = cart_items
        ctx['cart_total'] = sum(item['subtotal'] for item in cart_items)
        ctx['cart_count'] = sum(item['quantity'] for item in cart_items)
        ctx['show_modal'] = self.request.GET.get('sent') == '1'
        ctx['sent_email'] = self.request.GET.get('email', '')
        return ctx


class QuotationCartToggleView(View):
    """AJAX: agrega o quita un producto del carrito en sesión"""

    def post(self, request, pk):
        product_id = str(pk)
        action = request.POST.get('action', 'add')
        cart = request.session.get('quotation_cart', {})

        if action == 'add':
            cart[product_id] = cart.get(product_id, 0) + 1
        elif action == 'decrement':
            current = cart.get(product_id, 0)
            if current <= 1:
                cart.pop(product_id, None)
            else:
                cart[product_id] = current - 1
        elif action == 'remove':
            cart.pop(product_id, None)
        elif action == 'set':
            qty = int(request.POST.get('quantity', 1))
            if qty > 0:
                cart[product_id] = qty
            else:
                cart.pop(product_id, None)

        request.session['quotation_cart'] = cart

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'count': sum(cart.values())})

        return HttpResponseRedirect(reverse('app_quotations:quotation-build'))


class QuotationCreateFromCartView(FormView):
    """Procesa el formulario del cotizador y crea la cotización con todos los productos del carrito"""
    form_class = QuotationCartForm
    http_method_names = ['post']

    def form_valid(self, form):
        cart = self.request.session.get('quotation_cart', {})
        if not cart:
            messages.error(self.request, 'No hay productos en la cotización.')
            return HttpResponseRedirect(reverse('app_quotations:quotation-build'))

        quotation = QuotationRequest.objects.create(
            customer_name=form.cleaned_data['customer_name'],
            customer_email=form.cleaned_data['customer_email'],
            customer_phone=form.cleaned_data['customer_phone'],
            notes=form.cleaned_data['notes'],
        )

        products = Product.objects.filter(
            pk__in=[int(k) for k in cart.keys()], is_active=True
        )
        for product in products:
            qty = cart.get(str(product.pk), 0)
            if qty > 0:
                up = product.effective_price
                QuotationItem.objects.create(
                    quotation=quotation,
                    product=product,
                    product_name=product.name,
                    product_sku=product.sku,
                    quantity=qty,
                    unit_price=up,
                    subtotal=qty * up,
                )

        total = sum(qty * product.effective_price for product in products for qty in [cart.get(str(product.pk), 0)] if qty > 0)
        rows_html = ''.join(
            f'<tr><td>{p.name}</td><td>{p.sku}</td><td style="text-align:center">{cart.get(str(p.pk), 0)}</td>'
            f'<td style="text-align:right">S/ {p.effective_price:.0f}</td>'
            f'<td style="text-align:right">S/ {cart.get(str(p.pk), 0) * p.effective_price:.0f}</td></tr>'
            for p in products if cart.get(str(p.pk), 0) > 0
        )
        html = f"""
        <h2>Nueva cotización</h2>
        <p><strong>Cliente:</strong> {quotation.customer_name}<br>
        <strong>Email:</strong> {quotation.customer_email}<br>
        <strong>Teléfono:</strong> {quotation.customer_phone}</p>
        <p><strong>Notas:</strong><br>{quotation.notes or '—'}</p>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%">
        <thead style="background:#eee"><tr>
        <th>Producto</th><th>SKU</th><th>Cant</th><th>P.U.</th><th>Subtotal</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
        <tfoot><tr style="font-weight:bold">
        <td colspan="4" style="text-align:right">Total</td>
        <td style="text-align:right">S/ {total:.0f}</td>
        </tr></tfoot>
        </table>
        """
        send_mail(
            subject=f'Nueva cotización — {quotation.customer_name}',
            message='',
            html_message=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[quotation.customer_email, 'roberthbardales@gmail.com'],
            fail_silently=False,
        )

        del self.request.session['quotation_cart']
        return HttpResponseRedirect(reverse('app_quotations:quotation-build') + '?sent=1&email=' + quotation.customer_email)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for err in errors:
                messages.error(self.request, f'{err}')
        return HttpResponseRedirect(reverse('app_quotations:quotation-build'))


# =============================================================================
# VISTAS PÚBLICAS
# =============================================================================

class PublicProductDetailView(DetailView):
    model = Product
    template_name = 'quotations/public_product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related('images', 'specifications')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = PublicQuotationForm(initial={'product_id': self.object.pk, 'quantity': 1})
        sent_email = self.request.session.pop('quotation_sent', None)
        ctx['show_modal'] = sent_email is not None
        ctx['sent_email'] = sent_email or ''
        ctx['gallery'] = list(self.object.images.all())
        ctx['related_products'] = Product.objects.filter(
            is_active=True, category=self.object.category
        ).exclude(pk=self.object.pk).select_related(
            'category', 'brand'
        )[:4]
        return ctx


class CreateQuotationView(FormView):
    form_class = PublicQuotationForm
    http_method_names = ['post']

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=form.cleaned_data['product_id'], is_active=True)

        quotation = QuotationRequest.objects.create(
            customer_name=form.cleaned_data['customer_name'],
            customer_email=form.cleaned_data['customer_email'],
            customer_phone=form.cleaned_data['customer_phone'],
            notes=form.cleaned_data['notes'],
        )

        up = product.effective_price
        QuotationItem.objects.create(
            quotation=quotation,
            product=product,
            product_name=product.name,
            product_sku=product.sku,
            quantity=form.cleaned_data['quantity'],
            unit_price=up,
            subtotal=form.cleaned_data['quantity'] * up,
        )

        html = f"""
        <h2>Nueva cotización</h2>
        <p><strong>Cliente:</strong> {quotation.customer_name}<br>
        <strong>Email:</strong> {quotation.customer_email}<br>
        <strong>Teléfono:</strong> {quotation.customer_phone}</p>
        <p><strong>Notas:</strong><br>{quotation.notes or '—'}</p>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%">
        <thead style="background:#eee"><tr>
        <th>Producto</th><th>SKU</th><th>Cant</th><th>P.U.</th><th>Subtotal</th>
        </tr></thead>
        <tbody>
        <tr><td>{product.name}</td><td>{product.sku}</td><td style="text-align:center">{form.cleaned_data['quantity']}</td>
        <td style="text-align:right">S/ {up:.0f}</td>
        <td style="text-align:right">S/ {form.cleaned_data['quantity'] * up:.0f}</td></tr>
        </tbody>
        </table>
        """
        send_mail(
            subject=f'Nueva cotización — {quotation.customer_name}',
            message='',
            html_message=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[quotation.customer_email, 'roberthbardales@gmail.com'],
            fail_silently=False,
        )

        self.request.session['quotation_sent'] = form.cleaned_data['customer_email']
        return HttpResponseRedirect(
            reverse('app_quotations:public-product-detail', kwargs={'slug': product.slug})
        )

    def form_invalid(self, form):
        product_id = self.request.POST.get('product_id')
        if product_id:
            slug = Product.objects.filter(pk=product_id, is_active=True).values_list('slug', flat=True).first()
            if slug:
                for field, errors in form.errors.items():
                    for err in errors:
                        messages.error(self.request, f'{err}')
                return HttpResponseRedirect(
                    reverse('app_quotations:public-product-detail', kwargs={'slug': slug})
                )
        messages.error(self.request, 'Error al enviar la cotización. Verifica los datos.')
        return HttpResponseRedirect(reverse('app_home:index'))


# =============================================================================
# VISTAS ADMIN
# =============================================================================

class QuotationListView(AdministradorPermisoMixin, ListView):
    model = QuotationRequest
    template_name = 'quotations/quotation_list.html'
    context_object_name = 'quotations'
    paginate_by = 10

    def get_queryset(self):
        return QuotationRequest.objects.all().prefetch_related(
            Prefetch('items', queryset=QuotationItem.objects.select_related('product'))
        )


class QuotationDetailView(AdministradorPermisoMixin, DetailView):
    model = QuotationRequest
    template_name = 'quotations/quotation_detail.html'
    context_object_name = 'quotation'

    def get_queryset(self):
        return QuotationRequest.objects.prefetch_related(
            Prefetch('items', queryset=QuotationItem.objects.select_related('product'))
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = self.object.items.all()
        ctx['total'] = sum(item.subtotal for item in items)
        return ctx
