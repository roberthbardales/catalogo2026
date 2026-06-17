from django.db import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from applications.users.mixins import VentasPermisoMixin

from .forms import StockMovementForm
from .models import StockMovement


class MovementListView(VentasPermisoMixin, ListView):
    model = StockMovement
    template_name = 'inventory/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 10

    def get_queryset(self):
        qs = StockMovement.objects.select_related('product', 'created_by').order_by('-created')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                models.Q(product__name__icontains=q) | models.Q(note__icontains=q)
            )
        movement_type = self.request.GET.get('type', '').strip()
        if movement_type in (StockMovement.IN, StockMovement.OUT):
            qs = qs.filter(movement_type=movement_type)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['current_type'] = self.request.GET.get('type', '')
        return ctx


class MovementCreateView(VentasPermisoMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/movement_form.html'
    success_url = reverse_lazy('app_inventory:movement-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
