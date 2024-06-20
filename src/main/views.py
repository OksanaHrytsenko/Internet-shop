from django.shortcuts import render
from django.views.generic import TemplateView
from goods.models import Categories

class IndexView(TemplateView):
    template_name = "main/index.html"
    http_method_names = ["get"]


class AboutView(TemplateView):
    template_name = "main/about.html"
    http_method_names = ["get"]
    extra_context = {
        'title': 'Home - About us',
        'content': 'О нас',
        'text_on_page': 'Текст о том почему этот магазин такой классный, и какой хороший товар.'
    }


