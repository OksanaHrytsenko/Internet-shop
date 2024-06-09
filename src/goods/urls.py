from django.urls import path

from goods.views import CatalogView, ProductView

app_name = 'goods'

urlpatterns = [
    path("", CatalogView.as_view(), name="index"),
    path("product/", ProductView.as_view(), name="product"),

]
