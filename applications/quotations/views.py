from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, View

from applications.products.models import Product
from applications.users.mixins import AdministradorPermisoMixin
from applications.inventory.models import StockMovement

from .forms import PublicQuotationForm
from .models import QuotationItem, QuotationRequest


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
        return Product.objects.filter(is_active=True).select_related('category', 'brand')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = PublicQuotationForm(initial={'product_id': self.object.pk, 'quantity': 1})
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

        QuotationItem.objects.create(
            quotation=quotation,
            product=product,
            product_name=product.name,
            product_sku=product.sku,
            quantity=form.cleaned_data['quantity'],
            unit_price=product.price,
            subtotal=form.cleaned_data['quantity'] * product.price,
        )

        messages.success(
            self.request,
            'Cotización enviada correctamente. Nos pondremos en contacto pronto.'
        )
        return HttpResponseRedirect(reverse('app_quotations:quotation-thanks'))

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


class QuotationThanksView(TemplateView):
    template_name = 'quotations/thanks.html'


# =============================================================================
# VISTAS ADMIN
# =============================================================================

class QuotationListView(AdministradorPermisoMixin, ListView):
    model = QuotationRequest
    template_name = 'quotations/quotation_list.html'
    context_object_name = 'quotations'
    paginate_by = 10

    def get_queryset(self):
        qs = QuotationRequest.objects.all().prefetch_related(
            Prefetch('items', queryset=QuotationItem.objects.select_related('product'))
        )
        status = self.request.GET.get('status', '')
        if status in dict(QuotationRequest.STATUS_CHOICES):
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_status'] = self.request.GET.get('status', '')
        ctx['status_choices'] = QuotationRequest.STATUS_CHOICES
        return ctx


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
        ctx['status_choices'] = QuotationRequest.STATUS_CHOICES
        items = self.object.items.all()
        ctx['total'] = sum(item.subtotal for item in items)
        return ctx


class QuotationStatusUpdateView(AdministradorPermisoMixin, View):
    http_method_names = ['post']

    def post(self, request, pk):
        quotation = get_object_or_404(QuotationRequest, pk=pk)
        new_status = request.POST.get('status', '')
        if new_status in dict(QuotationRequest.STATUS_CHOICES):
            quotation.status = new_status
            quotation.save(update_fields=['status'])
            messages.success(request, f'Estado actualizado a "{quotation.get_status_display()}".')
        else:
            messages.error(request, 'Estado inválido.')
        return HttpResponseRedirect(reverse('app_quotations:quotation-detail', kwargs={'pk': pk}))
