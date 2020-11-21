from apps.shop.models import Product, Variant, Category
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.shop.serializers import ProductSerializer
from django.views.decorators.cache import cache_page



def catalogue(request, category=None):
    if category:
        category_param = category.split('/')
        category = Category.objects.get(slug=category_param[-1])
        categories = category.get_descendants(include_self=True)
        products = Product.objects.filter(category__in=categories)
    else:
        products = Product.objects.all()
        
    products = products.filter(in_stock=True)
    serializer = ProductSerializer(products, many=True)
    context = {
        'category' : category,
        'products' : serializer.data,
    }
    return render(request, 'shop/catalogue/catalogue.html', context)


def facebook_feed(request):
    products = Product.objects.filter(in_stock=True)
    return render(request, 'shop/xml/facebook.xml', {'products' : products}, content_type="application/xhtml+xml")