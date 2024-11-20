from django.urls import path
from authenticate.views import *

app_name = 'authenticate'

urlpatterns = [
    path('login/', auth_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_logout, name='logout'),
]