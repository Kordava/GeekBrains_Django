from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache


from basketapp.models import Basket
from mainapp.models import ProductCategory, Product

import random

from django.conf import settings
from django.core.cache import cache

from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse


# Create your views here.

...

def get_links_menu():
   if settings.LOW_CACHE:
       key = 'links_menu'
       links_menu = cache.get(key)
       if links_menu is None:
           links_menu = ProductCategory.objects.filter(is_active=True)
           cache.set(key, links_menu)
       return links_menu
   else:
       return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
   if settings.LOW_CACHE:
       key = f'category_{pk}'
       category = cache.get(key)
       if category is None:
           category = get_object_or_404(ProductCategory, pk=pk)
           cache.set(key, category)
       return category
   else:
       return get_object_or_404(ProductCategory, pk=pk)


def get_products():
   if settings.LOW_CACHE:
       key = 'products'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
   if settings.LOW_CACHE:
       key = f'product_{pk}'
       product = cache.get(key)
       if product is None:
           product = get_object_or_404(Product, pk=pk)
           cache.set(key, product)
       return product
   else:
       return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
   if settings.LOW_CACHE:
       key = 'products_orederd_by_price'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True,category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
   if settings.LOW_CACHE:
       key = f'products_in_category_orederd_by_price_{pk}'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(category__pk=pk, is_active=True,category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_random_product(products):
    my_list = list(products)
    return random.sample(my_list, len(my_list))
    # проще было бы set(my_list)

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True, category__is_active=True).exclude(pk=hot_product.pk).select_related('category')[:3]
    return same_products

def main(request, page=1):
    title = 'Главная'
    products = get_products()
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
    products = get_products_orederd_by_price()
    links_menu = get_links_menu()
    category = {'pk': 0, 'name': 'все'}

    if pk is not None:
        if pk == 0:
            products = get_products_orederd_by_price()

        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = get_products_in_category_orederd_by_price(pk)

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

def products_ajax(request, pk=None, page=1):
   if request.is_ajax():
       title = 'Продукты'
       products = get_products_orederd_by_price()
       links_menu = get_links_menu()
       category = {'pk': 0, 'name': 'все'}

       if pk is not None:
           if int(pk) == 0:
               products = get_products_orederd_by_price()

           else:
               category = get_category(int(pk))
               products = get_products_in_category_orederd_by_price(int(pk))

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
       result = render_to_string(
                    'mainapp/Templ/product_tab_content_type_main_data.html',
                    context=content,
                    request=request)

       return JsonResponse({'result': result})

def product_detail(request, pk=None):
    title = 'Подробно'
    links_menu = get_links_menu()
    product = get_product(pk)
    same_products = get_same_products(product)
    content = {
        'title': title,
        'categories': links_menu,
        'same_products': same_products,
        'product': product,
    }
    return render(request, 'mainapp/product-detail.html', content)


