from django import forms
from django.forms import inlineformset_factory

from .models import Brand, Category, Product, ProductImage, TechnicalSpecification


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'sku',
            'short_description',
            'description',
            'price',
            'stock',
            'image_main',
            'category',
            'brand',
            'tags',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_main': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'order', 'is_active']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto alternativo'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:80px'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TechnicalSpecificationForm(forms.ModelForm):
    class Meta:
        model = TechnicalSpecification
        fields = ['key', 'value', 'order', 'is_active']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Procesador'}),
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Intel i7'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:80px'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=1, can_delete=True
)

TechnicalSpecificationFormSet = inlineformset_factory(
    Product, TechnicalSpecification, form=TechnicalSpecificationForm, extra=1, can_delete=True
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'logo', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
