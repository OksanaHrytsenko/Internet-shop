from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Products


class CatalogView(TemplateView):
    template_name = "goods/catalog.html"
    http_method_names = ["get"]
    goods = Products.objects.all()
    extra_context = {
        'title': 'Home - Catalog',
        'goods': goods,
    }


class ProductView(TemplateView):
    template_name = "goods/product.html"
    http_method_names = ["get"]
