from django.shortcuts import render, redirect
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
