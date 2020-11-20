from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.http import JsonResponse
from apps.shop.models import Brand, Category, Variant
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
from django.views.decorators.csrf import csrf_exempt
import re



@csrf_exempt
@require_http_methods(["POST"])
def search(request):
    args = {}
    data = json.loads(request.body.decode())['search']
    products = {}
    product_name = []
    brands = []
    categories = []
    product_name = {}
    product_name_human = {}
    color = {}
    if len(data) > 0:
        for item in Variant.objects.all():
            name_parts = [part for part in [item.parent.brand.name, item.parent.name, item.color.name] if part != None]
            name = ' '.join(name_parts)
            
            # product_name.append(name)
            brand_word = ''
            color_word = ''
            category_word = ''
            for word in data.split(' '):
                # CATEGORY
                category_ratio = fuzz.token_sort_ratio(item.parent.category.name, word)
                if category_ratio > 70:
                    categories.append(item.parent.category.slug)
                    category_word = word
                    if item.pk not in products.keys():
                        products[item.pk] = {}
                        products[item.pk]['category_ratio'] = category_ratio
                # BRAND
                brand_ratio = fuzz.token_sort_ratio(item.parent.brand.name, word)
                if brand_ratio > 75:
                    brands.append(item.parent.brand.slug)
                    brand_word = word
                    if item.pk not in products.keys():
                        products[item.pk] = {}
                        products[item.pk]['brand_ratio'] = brand_ratio
                # COLOR
                if item.color != None:
                    color_ratio = fuzz.token_sort_ratio(item.color, word)
                    if color_ratio > 75:

                        color_word = word
                        if item.pk not in products.keys():
                            products[item.pk] = {}
                        products[item.pk]['color_ratio'] = color_ratio
                    # FULL MATCH
            if data in name:
                if item.pk not in products.keys():
                    products[item.pk] = {}
                products[item.pk]['full_match'] = 10000
            # NAME
            name = item.parent.name
            name_ratio = fuzz.token_sort_ratio(item.parent.name, data.replace(brand_word,''))
            if name_ratio > 75:
                if item.pk not in products.keys():
                    products[item.pk] = {}
                products[item.pk]['name_ratio'] = name_ratio
            if item.pk in products.keys():
                products[item.pk]['total'] = 0
                products[item.pk]['pk'] = item.pk

        # SET TOTAL RATIO
        for pk in products.keys():
            for ratio in products[pk]:
                if ratio != 'total':
                    products[pk]['total'] += products[pk][ratio]
            length = len(products[pk].keys()) - 1
            products[pk]['total'] = products[pk]['total'] / length
    

        # SORT BY TOTAL RATIO
        arr = list(products.values())
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j]['total'] < arr[j+1]['total']:
                    arr[j], arr[j+1] = arr[j+1], arr[j]

        args['products'] = []
        for product in arr:
            args['products'].append(Variant.objects.get(pk=product['pk']))

        args['brands'] = Brand.objects.filter(slug__in=brands)
        args['categories'] = Category.objects.filter(slug__in=categories)
    result = render_to_string('base/header/header__search__output.html', args)
    

    response = {'serarch' : result}
    return JsonResponse(response)