from django.urls import reverse
from project import settings
from apps.shop.models import Product, Variant
from apps.shop.serializers import ProductCartSerializer, VariantCartSerializer
import json


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {'products' : [], 'quantity' : 0, 'total' : 0}
        self.cart = cart
        

    def __iter__(self):
        for item in self.cart['products']:
            yield item

    def add(self, data):
        if data.get('product_id'):
            new = {
                'product_id' : int(data.get('product_id')) if len(data.get('product_id')) else None,
                'variant_id' : int(data.get('variant_id')) if data.get('variant_id') and len(data.get('variant_id')) else None,
                'quantity' : 1,
            }

            print(new)
            exists = False
            for item in self.cart['products']:
                if new['product_id'] == item['product_id'] and new['variant_id'] == item['variant_id']:
                    exists = True

            if exists == False:
                self.cart['products'].append(new)
        self.save()


    def data(self):
        exclude = []
        cart_data = {
            'products' : [], 
            'quantity' : 0, 
            'total' : 0,
        }
        for item in self.cart['products']:
            product = Product.objects.get(pk=item.get('product_id'))
            variant = product.variant.filter(pk=item.get('variant_id')).first()
            quantity = int(item.get('quantity'))
            total = quantity * product.price
            name = product.name
            if variant:
                name_parts = []
                if variant.name:
                    name_parts.append(variant.name)
                if variant.color:
                    name_parts.append(variant.color.name)
                if len(name_parts):
                   name += f" - {','.join(name_parts)}"
                
            cart_data['products'].append({
                'product' :  ProductCartSerializer(product).data,
                'variant' :  VariantCartSerializer(variant).data,
                'image' :    variant.image_xs if variant else product.image_xs,
                'link' :     variant.link if variant else product.link,
                'name' :     name,
                'quantity' : quantity,
                'total' :    total,
            })   
            cart_data['quantity'] += quantity
            cart_data['total'] += total
        return cart_data

    def save(self):
        self.session.modified = True

    def update(self, number, action=None, quantity=None):
        products = self.cart['products']
        product = products[int(number)]
        if not quantity:
            quantity = int(product['quantity'])
            if  action == 'plus' and quantity < 100:
                quantity += 1
            elif action == 'minus' and quantity > 1:
                quantity -= 1
        products[int(number)]['quantity'] = quantity
        self.cart['products'] = products
        self.save()

    def remove(self, number):
        del self.cart['products'][int(number)]
        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

