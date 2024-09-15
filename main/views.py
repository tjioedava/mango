from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from .forms import ProductForm
from .models import Product

def home(request):
    products = Product.objects.all()

    return render(request, 'home.html', {
        'products': products,
    })

def create_product(request):
    form = ProductForm(request.POST or None) 

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('main:home')

    return render(request, 'create-product.html', {
        'form': form,
    })

@require_http_methods(['GET',])
def show_products(request):

    format = request.GET.get('format', 'json')

    if format not in ['json', 'xml']:
        raise Http404()

    products = Product.objects.all()
    return HttpResponse(serialize(format, products), content_type=f'application/{format}')

@require_http_methods(['GET',])
def show_product_by_id(request, pk):

    format = request.GET.get('format', 'json')

    if format not in ['json', 'xml']:
        raise Http404()
    
    products = Product.objects.filter(pk=pk)

    if not products:
        return HttpResponse(f'Product with id {pk} does not exist')

    return HttpResponse(serialize(format, products), content_type=f'application/{format}')
    
