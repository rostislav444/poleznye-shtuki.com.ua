const cartProductsList = document.getElementById('cart_products_list') 
const orderProductsList = document.querySelector('.order__products-list')


function renderCart(data) {
    let tpl = nunjucks.renderString(document.getElementById('tpl_cart_list').innerHTML,  data);
    cartProductsList.innerHTML = tpl
    for (let obj of document.querySelectorAll('.cart__total')) {

        obj.innerHTML = data['total']
    }
    for (let obj of  document.querySelectorAll('.cart__quantity')) {
        obj.innerHTML = data['quantity']
    }
    
    if (orderProductsList != null) {
        tpl = nunjucks.renderString(document.getElementById('tpl_order_products').innerHTML,  data);
        
        orderProductsList.innerHTML = tpl
        let orderTotal = document.getElementById('order_total')
        if (orderTotal) {
            orderTotal.innerHTML = data['total']
        }
        if (parseInt(data['total']) == 0) {
            document.querySelector('.order__form__wrapper').style.display = "none"; 
        } else {
            document.querySelector('.order__form__wrapper').style.display = 'inline-block'
        }
    }

    CartInit()

}
// var cartData = fetchCartData()
// renderCart(cartData)

function fetchCartData() {
    let url = cartUrls['data']
    let csrf = Cookies.get()
    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("X-CSRFToken", csrf["csrftoken"]);
    request.send()
    request.onload = function () {
        let data = JSON.parse(request.responseText);
        renderCart(data)
    }
}  
fetchCartData()



function CartRequest(method, url, data) {
    let response = XHR(method, url, JSON.stringify(data))
        renderCart(response)
        if (orderProductsList == null) {
            pushbar.open('cart_sidebar')
        }
        
}


var timer
function CartAdd(product_id, variant_id, pixel_id) {
    let input = document.getElementById("product__quantity")
    let quantity = 1
    if (input != undefined) {
        quantity = input.value
    }
    let url = cartUrls['update']

    fbq('track', 'AddToCart', { 
        content_type: 'product',
        content_ids: pixel_id,
    });


    data = {
        'product_id' : product_id,
        'variant_id' : variant_id,
        'quantity' : quantity,
        'update' :   false,
    }
    window.clearTimeout(timer)
    timer = window.setTimeout(CartRequest, 500, 'POST', url, data);
}

function CartUpdate(input) {
    let url = cartUrls['update']
    data = {
        'product_id' : input.dataset.product_id,
        'variant_id' : input.dataset.variant_id,
        'quantity' : input.value,
        'update' :   true,
    }
    window.clearTimeout(timer)
    timer = window.setTimeout(CartRequest, 500, 'POST', url, data);
}

function CartDelete(obj) {
    url = cartUrls['delete']
    data = {
        'product_id' : obj.dataset.product_id,
        'variant_id' : obj.dataset.variant_id,
    }
    CartRequest('POST', url, data)
}


function CartClear() {
    uurl = cartUrls['clear']
    CartRequest('GET', url, data)
}


var productBuyButton = document.querySelectorAll('.btn__add-to-cart')
for (let i = 0; i < productBuyButton.length; i++) {
    let btn = productBuyButton[i];
    btn.addEventListener('click', function() {
        let product_id = btn.dataset.product_id
        let variant_id = btn.dataset.variant_id
        let pixel_id = btn.dataset.pixel_id
        CartAdd(product_id, variant_id, pixel_id)
    })
    
}






function GetItem(object) {
    let parent = object.parentElement
    let counter = 0
    while (true) {
        if (Object.values(parent.classList).includes('item')) {
            return parent
        } else {
            counter += 1
            parent = parent.parentElement
            if (counter > 10) {
                return false
            } 
        }
    }
}





function CartInit() {
    Counter()
}


function CartCounter(object, math) {
    let url = baseUrl + '/cart/add-update'

    let item = GetItem(object)  
    let input = item.querySelector('input')
    let total = item.querySelector('span.total')
    if (parseInt(input.value) < parseInt(input.max)) {
        if (math == 'plus') {
            input.value = parseInt(input.value) + 1;
        } else if (math == 'minus') {
            if (input.value > 1) {
                input.value = parseInt(input.value) - 1;
            }
        } 
    }
    total.innerHTML = parseInt(total.dataset.price) * input.value
    data = {
        'product_id' : input.dataset.product_id,
        'variant_id' : input.dataset.variant_id,
        'option_id' :  input.dataset.option_id,
        'quantity' :   input.value,
        'update' :     'true',
        'redirect' :   'false',
    }
    method = 'POST'
    window.clearTimeout(timer)
    timer = window.setTimeout(CartRequest, 500, method, url, data);
}


