from .cart import Cart

def cart(request):
    cart = Cart(request)
    print(cart.cart)
    return {'cart': cart.data()}