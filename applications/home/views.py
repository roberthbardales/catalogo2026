from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'home/index.html'


class AboutView(TemplateView):
    template_name = 'home/about.html'


class ProductsView(TemplateView):
    template_name = 'home/products.html'


class CategoriesView(TemplateView):
    template_name = 'home/categories.html'


class BrandsView(TemplateView):
    template_name = 'home/brands.html'


class WarrantyView(TemplateView):
    template_name = 'home/warranty.html'


class ContactView(TemplateView):
    template_name = 'home/contact.html'
