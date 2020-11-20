from django.shortcuts import redirect, render
from django.urls import reverse
from .cart import Cart
from django.views.decorators.http import require_http_methods
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



class CartView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def initial(self, request, *args, **kwargs):
        self.cart = Cart(request)
        super(CartView, self).initial(request, *args, **kwargs)
      

    def add(self, request):
        print('cart add', reverse('order:order'))
        cart = Cart(request)
        cart.add(request.POST)
        return redirect(reverse('order:order'))

    def update(self, request):
        data = request.data
        cart = self.cart
        cart.update(
            number=data.get('number'), 
            action=data.get('action'), 
            quantity=data.get('quantity')
        )
        path = request.META.get('HTTP_REFERER')
        if path:
            return redirect(path)
        else:
            return redirect(reverse('order:order'))

    def clear(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect('/')

    def remove(self, request, number):
        cart = Cart(request)
        cart.remove(number)
        data = cart.data()
        if int(data.get('quantity')) == 0:
            return redirect('/')
        path = request.META.get('HTTP_REFERER')
        if path:
            return redirect(path)
        else:
            return redirect(reverse('order:order'))
        


