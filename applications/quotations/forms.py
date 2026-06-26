from django import forms


class QuotationCartForm(forms.Form):
    customer_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': ''})
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': ''})
    )
    customer_phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': ''})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2, 'placeholder': ''})
    )


class PublicQuotationForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )
    customer_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    customer_phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': ''})
    )
