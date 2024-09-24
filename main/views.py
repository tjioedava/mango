from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm
from .models import Product

@login_required(login_url='/log-in')
def home(request):
    products = Product.objects.all()

    return render(request, 'home.html', {
        'products': products,
    })

@login_required(login_url='/log-in')
def create_product(request):
    form = ProductForm(request.POST or None) 

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('main:home')

    return render(request, 'create-product.html', {
        'form': form,
    })

@login_required(login_url='/log-in')
def show_products(request):

    format = request.GET.get('format', 'json')

    if format not in ['json', 'xml']:
        raise Http404()

    products = Product.objects.all()
    return HttpResponse(serialize(format, products), content_type=f'application/{format}')

def show_product_by_id(request, pk):

    format = request.GET.get('format', 'json')

    if format not in ['json', 'xml']:
        raise Http404()
    
    products = Product.objects.filter(pk=pk)

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
                return HttpResponseRedirect(request.GET.get('next', reverse('main:home')))
            
        messages.error(request, 'Empty or incorrect credentials!')

    return render(request, 'log-in.html', {
        'form': form,
    })

@require_http_methods(['POST',])
def log_out(request):
    logout(request)
    return redirect('main:log-in')
