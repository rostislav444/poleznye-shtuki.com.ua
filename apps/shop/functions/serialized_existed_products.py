
from apps.shop.serializers import ProductCartSerializer, VariantCartSerializer
from apps.shop.models import Product


def serializedExistedProducts(items_list, cart=False):
    if cart: data = { 'products' : [], 'quantity' : 0, 'total' : 0 }
    else:    data = { 'products' : [] }
    remove_indexes = []
    products = Product.objects.filter(
        pk__in=[int(item['product_id']) for item in items_list]
    )

    def cart_product(serializer, quantity):
        price = serializer['price']
        serializer['quantity'] = quantity
        serializer['total'] = quantity * price
        data['total'] += serializer['total']
        data['quantity'] += quantity
        return serializer

    def serialize_product(item):
        product_id, variant_id = item['product_id'], item['variant_id']
        product = products.get(pk=int(product_id))
        
        if variant_id != None:
            variant = product.variant.get(pk=int(variant_id))
            serializer = VariantCartSerializer(variant).data
        else:
            serializer = ProductCartSerializer(product).data
        return serializer
        
    # SERIALIZE PRODUCTS
    for n, item in enumerate(items_list):
        try: 
            serializer = serialize_product(item)
            if cart:  
                serializer = cart_product(serializer, item['quantity'])
            
        except: remove_indexes.append(n)
        
        data['products'].append(serializer)
    # REMOVE DELETED PRODUCTS FROM LIST
    for i in remove_indexes:
        try: del items_list[i]
        except: pass
    return items_list, data



