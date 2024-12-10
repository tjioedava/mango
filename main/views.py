from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import strip_tags
from .models import Product
from .utils import validate_product_form_input, validate_user_creation_input
import datetime
import json

@login_required(login_url='/log-in')
def home(request):
    return render(request, 'home.html', dict())

@login_required(login_url='/log-in')
def create_product(request):
    if request.method == 'POST':
        name = strip_tags(request.POST.get('name'))
        price = request.POST.get('price')
        description = strip_tags(request.POST.get('description'))

        result = validate_product_form_input(name, price, description)
        if result[0]:
           Product.objects.create(user=request.user, name=name, price=price, description=description) 
           messages.success(request, 'Product created successfully')
           return redirect('main:home')
        
        for message in result[1]:
            messages.error(request, message)

    return render(request, 'create-product.html')

@require_http_methods(['POST',])
def create_product_ajax(request):
    
    data = json.loads(request.body.decode('utf-8'))

    name = strip_tags(data.get('name'))
    price = data.get('price')
    description = strip_tags(data.get('description'))
    
    result = validate_product_form_input(name, price, description)

    if result[0]:
        Product.objects.create(user=request.user, name=name, price=price, description=description)
        messages.success(request, 'Product created successfully')
    for message in result[1]:
        messages.error(request, message)
    
    messages_response = [{'level_tag': message.level_tag, 'message': message.message} for message in list(messages.get_messages(request))]
    return JsonResponse({'success': result[0], 'messages': messages_response})


@login_required(login_url='/log-in')
def edit_product(request, pk):
    products = Product.objects.filter(user=request.user, id=pk)
    if len(products) == 0:
        return HttpResponseNotFound()
    product = products[0]

    if request.method == 'POST':
        name = strip_tags(request.POST.get('name'))
        price = request.POST.get('price')
        description = strip_tags(request.POST.get('description'))
        result = validate_product_form_input(name, price, description)
        if result[0]:
            product.name = name
            product.price = price
            product.description = description
            product.save()
            messages.success(request, 'Product edited successfully')
            return redirect('main:home')
        for message in result[1]:
            messages.info(request, message)

    return render(request, 'edit-product.html', {
        'product': product,
    })

@require_http_methods(['POST',])
def delete_product(request, pk):
    products = Product.objects.filter(user=request.user, id=pk)
    if len(products) == 0:
        return HttpResponseNotFound()
    
    product = products[0]

    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('main:home')

@login_required(login_url='/log-in')
def show_products(request):

    format = request.GET.get('format', 'json')

    if format not in ['json', 'xml']:
        return HttpResponseNotFound()
    
    own = request.GET.get('own', 'true')

    if own not in ['true', 'false']:
        return HttpResponseNotFound()
    
    if own == 'true':
        products = Product.objects.filter(user=request.user)
    else: 
        products = Product.objects.all()
    
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
            messages.success(request, 'Account registered successfully')
            return redirect('main:log-in')
        
        for message in result[1]:
            messages.error(request, message)

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
            messages.success(request, 'Successfully logged in')
            return response
        
        messages.error(request, 'Invalid credentials')

    return render(request, 'log-in.html', dict())

@require_http_methods(['POST',])
def log_out(request):
    logout(request)
    response = redirect('main:log-in')
    response.delete_cookie('last_log_in')
    messages.success(request, 'Successfully logged out')
    return response

@csrf_exempt
def create_product_mobile(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        product = Product.objects.create(
            name=data["name"],
            user=request.user,
            price= int(data["price"]),
            description=data["description"],
        )

        product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)