from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product

import random

# Create your views here.

def get_random_product(products):
    my_list = list(products)
    return random.sample(my_list, len(my_list))
    # проще было бы set(my_list)

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True, category__is_active=True).\
    exclude(pk=hot_product.pk)[:3]
    return same_products

def main(request, page=1):
    title = 'Главная'
    products = Product.objects.filter(is_active=True, category__is_active=True)
    hot_products = get_random_product(products)
    category = {'pk': 0, 'name': 'все'}

    paginator = Paginator(hot_products, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': title,
        'category': category,
        'hot_products': products_paginator,
    }
    return render(request, 'mainapp/index.html', content)

def contact(request):
    title = 'Контакты'
    content = {
        'title': title,
        'city': 'CALIFORNIA',
        'phone': '1900 - 1234 -5678',
        'mail': 'info@interior.com',
        'adres': '12 W 1st St, 90001 Los Angeles, California',
    }
    return render(request, 'mainapp/contact.html', content)


def products(request, pk=None, page=1):
    title = 'Продукты'
    products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
    links_menu = ProductCategory.objects.all()
    category = {'pk': 0, 'name': 'все'}

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')

        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

    hot_products = get_random_product(products)

    paginator = Paginator(hot_products, 6)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': title,
        'categories': links_menu,
        'category': category,
        'hot_products': products_paginator,
    }


    return render(request, 'mainapp/products.html', content)

def product_detail(request, pk=None):
    title = 'Подробно'
    links_menu = ProductCategory.objects.all()
    product = get_object_or_404(Product, pk=pk)
    same_products = get_same_products(product)
    content = {
        'title': title,
        'categories': links_menu,
        'same_products': same_products,
        'product': product,
    }
    return render(request, 'mainapp/product-detail.html', content)


