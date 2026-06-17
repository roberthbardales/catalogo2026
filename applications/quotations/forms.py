from django import forms


class PublicQuotationForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )
    customer_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'})
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: juan@ejemplo.com'})
    )
    customer_phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 999 888 777'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentarios adicionales (opcional)'})
    )
