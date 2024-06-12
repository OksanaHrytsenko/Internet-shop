from django.urls import path
from goods.views import catalog, get_product

app_name = 'goods'

urlpatterns = [
    path("search/", catalog, name="search"),
    path("<slug:category_slug>/", catalog, name="index"),
    path("product/<slug:product_slug>/", get_product, name="product"),
]
