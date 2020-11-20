from apps.shop.models import Variant
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
import json


def ReturnCartData(request, url=None):
    # variant = Variant.objects.get(pk=int(data['variant_id']))
    cart = Cart(request)

    cart.total = cart.total()
    list_html =  render_to_string('shop/cart/cart__list.html', {'cart':cart})
    total_html = render_to_string('shop/cart/cart__total.html', {'cart':cart})
    order_list_html =  render_to_string('orders/order__productlist.html', {'cart':cart})
    response = {
        'url'   : 'cart',
        'list_html' : list_html,
        'order_list_html' : order_list_html,
        'total_html' : total_html,
        'total' : cart.total
    }
    response = json.dumps(response, ensure_ascii=False).encode('utf8')
    response = json.loads(response.decode('utf8'))
    return JsonResponse(response, safe=False)


@csrf_exempt
def CartAddUpdate(request, update=False):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.loads(request.body.decode())
        if data['update'] == 'true':
            update = True
        cart.add(data, update)
        return ReturnCartData(request)
    else:
        return HttpResponse(status=500)


@csrf_exempt
def CartDelete(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        cart = Cart(request)
        cart.remove(data['variant_id'])
        return ReturnCartData(request)
    else:
        return HttpResponse(status=500)
        

@csrf_exempt
def CartClear(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponse(status=200)
    if request.method == 'POST':
        return HttpResponse(status=200)
    else:
        referer = request.META.get('HTTP_REFERER')
        if referer is not None:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('/')



