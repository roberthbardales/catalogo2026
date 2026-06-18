from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductTag,
    TechnicalSpecification,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class TechnicalSpecificationInline(admin.TabularInline):
    model = TechnicalSpecification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'brand', 'category', 'price', 'sale_price', 'stock', 'is_active')
    list_filter = ('is_active', 'brand', 'category', 'tags')
    search_fields = ('name', 'sku', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)
    inlines = [ProductImageInline, TechnicalSpecificationInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'is_active')
    list_filter = ('is_active', 'product')


@admin.register(TechnicalSpecification)
class TechnicalSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value', 'order', 'is_active')
    list_filter = ('is_active', 'product')
    search_fields = ('key', 'value', 'product__name')
