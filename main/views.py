from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm
from .models import Product
import datetime

@login_required(login_url='/log-in')
def home(request):
    products = Product.objects.filter(user=request.user)

    last_log_in = request.COOKIES['last_log_in']
    point_index = last_log_in.find('.')
    last_log_in = last_log_in[0: point_index]

    return render(request, 'home.html', {
        'last_log_in': last_log_in,
        'products': products,
    })

@login_required(login_url='/log-in')
def create_product(request):
    form = ProductForm(request.POST or None) 

    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('main:home')

    return render(request, 'create-product.html', {
        'form': form,
    })

@login_required(login_url='/log-in')
def edit_product(request, pk):
    products = Product.objects.filter(user=request.user, id=pk)
    if len(products) == 0:
        return HttpResponseNotFound()
    product = products[0]
    form = ProductForm(request.POST or None, instance=product)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('main:home')

    return render(request, 'edit-product.html', {
        'form': form,
    })

@require_http_methods(['POST',])
def delete_product(request, pk):
    products = Product.objects.filter(user=request.user, id=pk)
    if len(products) == 0:
        return HttpResponseNotFound()
    
    product = products[0]

    product.delete()
    return redirect('main:home')

@login_required(login_url='/log-in')
def show_products(request):

    format = request.GET.get('format', 'json')

    if format not in ['json', 'xml']:
        return HttpResponseNotFound()

    products = Product.objects.filter(user=request.user)
    return HttpResponse(serialize(format, products), content_type=f'application/{format}')

@login_required(login_url='/log-in')
def show_product_by_id(request, pk):

    format = request.GET.get('format', 'json')

    if format not in ['json', 'xml']:
        return HttpResponseNotFound()
    
    products = Product.objects.filter(user=request.user, pk=pk)

    if not products:
        return HttpResponse(f'Product with id {pk} does not exist')

    return HttpResponse(serialize(format, products), content_type=f'application/{format}')

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('main:log-in')
        else:
            ...
        
    return render(request, 'register.html', {
        'form': form,
    })

def log_in(request):

    #if user is already logged in, not anonymous
    if request.user.is_authenticated:
        return redirect('main:home')

    form = AuthenticationForm(data = request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                #return to the url embedded by login_required decorator or home url
                response = HttpResponseRedirect(request.GET.get('next', reverse('main:home')))
                response.set_cookie('last_log_in', datetime.datetime.now(), 60 * 60 * 24 * 7)
                return response
            
        messages.error(request, 'Empty or incorrect credentials!')

    return render(request, 'log-in.html', {
        'form': form,
    })

@require_http_methods(['POST',])
def log_out(request):
    logout(request)
    response = redirect('main:log-in')
    response.delete_cookie('last_log_in')
    return response