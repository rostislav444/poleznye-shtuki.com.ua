from django.shortcuts import render
from apps.shop.models import Product
from apps.shop.serializers import ProductSerializer
from apps.core.models import HomeSlider1, HomeSlider2, HomeSlider3


def home(request):
    products = Product.objects.filter(in_stock=True)
    args = {
        'products_popular' : ProductSerializer(products.order_by('view')[:24], many=True).data,
        'products_newest' :  ProductSerializer(products.order_by('-date')[:24], many=True).data,
        'home_slider_1' : HomeSlider1.objects.all(),
        'home_slider_2' : HomeSlider2.objects.all(),
        'home_slider_3' : HomeSlider3.objects.all(),
    }
    return render(request, 'shop/home/home.html', args)