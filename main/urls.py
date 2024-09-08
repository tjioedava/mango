from django.urls import path
from django.http import HttpResponse
from .views import *

app_name = 'main'

urlpatterns = [
    path('', lambda request: HttpResponse('Hello, World!'), dict()),
]