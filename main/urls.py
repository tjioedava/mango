from django.urls import path, reverse
from django.shortcuts import HttpResponseRedirect
from .views import home

app_name = 'main'

urlpatterns = [
    path('', lambda request: HttpResponseRedirect(reverse('main:home')), name='default'),
    path('home', home, name='home'),
]