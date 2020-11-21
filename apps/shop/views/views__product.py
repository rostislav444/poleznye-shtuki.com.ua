from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views import View
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.template.loader import render_to_string
from django.http import Http404, JsonResponse
from django.urls import reverse
from apps.shop.models import Product, Variant
from apps.shop.serializers import ProductSerializer
from apps.shop.functions.serialized_existed_products import serializedExistedProducts

from apps.order.models import Order, OrderProduct
from apps.comments.models import Comment, CommentImages, CommentReply, Question, QuestionReply
import requests 
from project.settings import DROP1_API_TOKEN
import json, re
import urllib
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



def makeRequest():
    url = "https://drop1.top/api/ds_orders"
    api_key = DROP1_API_TOKEN
    data = {
        'name' : 'Test',
        'lastname' : 'Test',
        'phone' : '380000000000',
        'delivery_city' : 'Kiev',
        'delivery_warehouses' : 188,
        'processing_type_id' : 2,
        'products[0][product_id]' : 3408,
        'products[0][quantity]' : 1,
        'products[0][price]' : 590,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept" : "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        response = requests.post(url, params=data, headers=headers)
        return response.json()
    except:
        return ''
    
    




def set_watchlist(request, product_id, variant_id=None):
    # def product_exists(item_list, product_id, variant_id):
    #     for n, item in enumerate(item_list):
    #         if item['product_id'] == product_id and item['variant_id'] == variant_id:
    #             return n
    #     return None
    # def get_session_list(key):
    #     if key not in request.session.keys():
    #         request.session[key] = []
    #     return request.session[key]

    # def add_or_update(product, product_list, n):
    #     if n != None:
    #         del product_list[n]
    #     product_list.insert(0, product)
    #     return product_list
            
    # product = {
    #     'product_id' : product_id, 
    #     'variant_id' : variant_id
    # }
    # watchlist= get_session_list('watchlist')
    # n = product_exists(watchlist, product_id, variant_id)
    # request.session['watchlist'] = add_or_update(product, watchlist, n)

    # items, data = serializedExistedProducts(request.session['watchlist'])
    # request.session['watchlist'] = items
    return JsonResponse({ 'watchlist' : []})




def watchlist(request):
    if 'watchlist' not in request.session.keys():
        request.session['watchlist'] = []
    # watchlist = request.session['watchlist']
    # items, data = serializedExistedProducts(watchlist)
    # request.session['watchlist'] = items
    return JsonResponse({ 'watchlist' : [] })



class ProductPage(viewsets.ViewSet):
    context = {}
    permission_classes = [AllowAny]

    def redirect_to_product(self, product, variant=None, page=None):
        kwargs = {
            'slug':product.slug, 
            'category':product.category_tree_slug, 
            'product_id':product.pk,
        }
        if variant: kwargs['variant_id'] = variant.pk
        if page:    kwargs['page'] = page
        return redirect(reverse('shop:product', kwargs=kwargs))


    def get_product(self, product_id, variant_id=None):
        product, variant = Product.objects.get(pk=product_id), None
        variants = product.variant.all()
        if len(variants):
            if variant_id:
                variant = variants.get(pk=variant_id)
            else:
                variant = variants.first()
        self.context = {'product' : product, 'variant' : variant}
        return product, variant


    # PAGES
    def page(self, request, category, slug, product_id, variant_id=None, page=None, api=False):
        product, variant = self.get_product(product_id, variant_id)
        if variant and variant_id==None:
            return self.redirect_to_product(product, variant, page)
        if page:
            return render(request, f"shop/product/pages/{page}__page.html", self.context)
        else:
            if request.user.is_authenticated == False:
                Product.objects.filter(pk=product.pk).update(view=product.view+1)
            return render(request, 'shop/product/pages/description__page.html', self.context)


    # COMMWNTS
    def comment_form(self, request, *args, **kwargs):
        if request.user.is_authenticated == False:
            return redirect(reverse('user:login')+'?redirect='+request.path)
        product, variant = self.get_product(kwargs.get('product_id'), kwargs.get('variant_id'))
        if request.method == 'POST':
            data = request.data
            commnent = Comment(
                user = request.user,
                product = product,
                rate = int(data['rate']),
                text = data['text'],
                text_plus = data['text_plus'],
                text_minus = data['text_minus'],
            )
            commnent.save()
            return redirect(reverse(
                'shop:product', kwargs={'slug':product.slug, 'category':product.category_tree_slug, 'product_id':product.pk, 'page':'comments'}
            ))
        return render(request, 'shop/product/pages/comments__from.html', self.context)

    def comment_reply(self, request, *args, **kwargs):
        return render(request, 'shop/product/pages/comments__page.html', self.context)


    # QUESTIONS
    def question_form(self, request, *args, **kwargs):
        if request.user.is_authenticated == False:
    
            return redirect(reverse('user:login'))
        product, variant = self.get_product(kwargs.get('product_id'), kwargs.get('variant_id'))
        if request.method == 'POST':
            data = request.data
            question = Question(
                user = request.user,
                product = product,
                text = data['text'],
            )
            question.save()
            return redirect(reverse(
                'shop:product', kwargs={'slug':product.slug, 'category':product.category_tree_slug, 'product_id':product.pk, 'page':'questions'}
            ))
        return render(request, 'shop/product/pages/questions__form.html', self.context)
    
    def question_reply(self, request, *args, **kwargs):
        return render(request, 'shop/product/pages/question__page.html', self.context)





def send_suplier_request(product, order):
    supliers = {}
    if product.suplier is not None:
        if product.suplier not in supliers.keys():
            supliers[product.suplier] = []
        supliers[product.suplier].append({
            'product_id' : int(product.suplier_id),
            'quantity' : 1,
            'price' : product.price,
        })
    for key, products in supliers.items():
        meth = getattr(Supliers(), key)
        kwargs = {'order' : order, 'products' : products}
        response = meth(**kwargs)
        Order.objects.filter(pk=order.pk).update(comment=str(response))



def product_lp(request, slug, product_id, variant_id=None):
    
    args = {}
    try: 
        product = Product.objects.get(pk=product_id)
        if variant_id != None:
            variant = Variant.objects.get(pk=variant_id)
        else: variant = None
    except:
        return redirect('/')
    Product.objects.filter(pk=product.pk).update(view=product.view+1)

    if request.method == 'POST':
        data = request.POST
        order = Order(
            name = data.get('name'),
            phone = data.get('phone'),
            phone_number = int(re.sub("\D", "", data.get('phone'))),
        )
        order.save()
        order_product = OrderProduct(
            order = order,
            product = product,
            price = product.price,
        )
        order_product.save()
        send_suplier_request(product, order)
        return redirect(reverse('shop:product_lp_success', kwargs={'slug' : product.slug, 'product_id' : product.pk}))

    args['product'] = product
    args['variant'] = variant
    return render(request, 'shop/product_lp/product.html', args)


def product_lp_success(request, slug, product_id, variant_id=None):
    args = {}
    try: 
        product = Product.objects.get(pk=product_id)
        if variant_id != None:
            variant = Variant.objects.get(pk=variant_id)
        else: variant = None
    except:
        return redirect('/')
    args['product'] = product
    args['variant'] = variant
    return render(request, 'shop/product_lp/order_success.html', args)


