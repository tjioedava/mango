from django.urls import path
from django.shortcuts import redirect
from .views import *

app_name = 'main'

urlpatterns = [
    path('', lambda request: redirect('main:home'), name='default'),
    path('home', home, name='home'),
    path('create-product', create_product, name='create-product'),
    path('edit-product/<uuid:pk>', edit_product, name='edit-product'),
    path('delete-product/<uuid:pk>', delete_product, name='delete-product'),
    path('show-products', show_products, name='show-products'),
    path('show-product-by-id/<uuid:pk>', show_product_by_id, name='show-product-by-id'),
    path('register', register, name='register'),
    path('log-in', log_in, name='log-in'),
    path('log-out', log_out, name='log-out'),
]