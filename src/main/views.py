from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "main/index.html"
    http_method_names = ["get"]


class AboutView(TemplateView):
    template_name = "main/about.html"
    http_method_names = ["get"]
    extra_context = {
        'title': 'Home - About us',
        'content': 'About us',
        'text_on_page': 'This is the best shop with the best products,we  have everything you were looking for'
    }


