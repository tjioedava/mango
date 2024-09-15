from django.urls import path, reverse
from django.shortcuts import HttpResponseRedirect
from .views import *

app_name = 'main'

urlpatterns = [
    path('', lambda request: HttpResponseRedirect(reverse('main:home')), name='default'),
    path('home', home, name='home'),
    path('create-product', create_product, name='create-product'),
    path('show-products', show_products, name='show-products'),
    path('show-product-by-id/<str:pk>', show_product_by_id, name='show-product-by-id'),
]