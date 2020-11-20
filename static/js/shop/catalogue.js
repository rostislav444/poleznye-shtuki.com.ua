var catalogueProduct = document.querySelectorAll('.catalogue__product')


for (let i = 0; i < catalogueProduct.length; i++) {
    let product = catalogueProduct[i]
    let image = product.querySelector('.catalogue__product__image')
    let aTags = product.querySelectorAll('a')
    for (let radio of product.querySelectorAll('input[type="radio"]')) {
        console.log(radio);
        radio.onchange = () => {
            let variant = radio.parentNode.querySelector('li')
            image.style.backgroundImage = 'url(' + variant.dataset.image + ')'
            for (let a of aTags) {
                a.href = variant.dataset.url
            }
        }
    }
    
}

