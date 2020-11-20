from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from apps.order.models import Order, OrderProduct
from apps.shop.models import Product, Variant, Supliers
from apps.shop.functions import serializedExistedProducts
from project import settings
from collections import OrderedDict 
from apps.cart.cart import Cart
import re


class OrderView(View):
    def get(self, request):
        args = {}
        cart = Cart(request)
        if cart.data().get('quantity') == 0:
            try:    return redirect(request.META.get('HTTP_REFERER'))
            except: return redirect('/')
        return render(request, 'order/order.html', args)

    def post(self, request, product_id=None, variant_id=None):
        post = request.POST
        order = Order(
            name = post.get('name'),
            surname = post.get('surname'),
            patronymic = post.get('patronymic') if 'patronymic' in post else '',
            phone_number = int(re.sub("\D", "", post.get('phone'))),
            phone = post.get('phone'),
            city =  post.get('city'),
            branch_number = post.get('branch_number'),
        )
        order.save()
        supliers = {}

        cart = request.session.get(settings.CART_SESSION_ID)
        cart_products = cart['products']
        if len(cart_products) == 0 and product_id is not None:
            cart_products.append({
                'product_id': product_id, 'variant_id' : variant_id, 'quantity' : 1
            })
        
        for item in cart['products']:
            product_id, variant_id  = item['product_id'], item['variant_id']
            product = Product.objects.get(pk=int(product_id))
            if variant_id is not None:
                variant = Variant.objects.get(pk=variant_id)
            else:
                variant = None
            

            if product.suplier is not None:
                if product.suplier not in supliers.keys():
                    supliers[product.suplier] = []
                supliers[product.suplier].append({
                    'product_id' : int(product.suplier_id),
                    'quantity' : int(item['quantity']),
                    'price' : product.price,
                    'color' : variant.color if variant is not None else '-',
                })

            order_product = OrderProduct(
                order=order,
                product=product,
                variant=variant,
                quantity=int(item['quantity']),
                price=product.price
            )
            order_product.save()

        for key, products in supliers.items():
            meth = getattr(Supliers(), key)
            kwargs = {'order' : order, 'products' : products}
            response = meth(**kwargs)
            Order.objects.filter(pk=order.pk).update(comment=str(response))
        del request.session[settings.CART_SESSION_ID]
        return redirect('order:order-success')




