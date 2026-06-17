from django import forms

from applications.products.models import Product

from .models import StockMovement


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'note']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del movimiento (opcional)'}),
        }
        labels = {
            'product': 'Producto',
            'movement_type': 'Tipo de movimiento',
            'quantity': 'Cantidad',
            'note': 'Nota',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True).select_related('category', 'brand').order_by('name')
        self.fields['product'].label_from_instance = lambda obj: f'{obj.name} ({obj.sku}) — S/ {obj.price} — Stock: {obj.stock}'

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        movement_type = cleaned_data.get('movement_type')
        quantity = cleaned_data.get('quantity')

        if product and movement_type == StockMovement.OUT and quantity:
            if quantity > product.stock:
                raise forms.ValidationError(
                    f'Stock insuficiente. "{product.name}" tiene {product.stock} unidades disponibles, '
                    f'pero solicitaste {quantity}.'
                )
        return cleaned_data
