from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from .utils import validate_product_form_input, validate_user_creation_input
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
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        result = validate_product_form_input(name, price, description)
        if result[0]:
           Product.objects.create(user=request.user, name=name, price=price, description=description) 
           return redirect('main:home')
        
        for message in result[1]:
            messages.info(message)

    return render(request, 'create-product.html')

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password-confirmation')

        result = validate_user_creation_input(username, password, password_confirmation)
        #if the valid flag is True:
        if result[0]:
            #using create_user method to not store the password in raw (hashing algo.)
            User.objects.create_user(username=username, password=password)
            return redirect('main:log-in')
        
        for message in result[1]:
            messages.info(request, message)

    return render(request, 'register.html', dict())

def log_in(request):

    #if user is already logged in, not anonymous
    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None: 
            login(request, user)
            #return to the url embedded by login_required decorator or home url
            response = redirect(request.GET.get('next', 'main:home'))
            response.set_cookie('last_log_in', datetime.datetime.now(), 60 * 60 * 24 * 7)
            return response
        
        messages.info(request, 'Invalid credentials')

    return render(request, 'log-in.html', dict())

@require_http_methods(['POST',])
def log_out(request):
    logout(request)
    response = redirect('main:log-in')
    response.delete_cookie('last_log_in')
    return response