from django.contrib import admin

from .models import QuotationItem, QuotationRequest


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'product_sku', 'quantity', 'unit_price', 'subtotal']


@admin.register(QuotationRequest)
class QuotationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'created']
    list_filter = ['created']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['customer_name', 'customer_email', 'customer_phone', 'notes', 'created', 'modified']
    inlines = [QuotationItemInline]
