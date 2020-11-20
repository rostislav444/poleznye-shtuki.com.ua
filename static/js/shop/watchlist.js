function WarchlistSwiper() {
    var swiper = new Swiper('.watchlist-container', {
        slidesPerView: 5,
        spaceBetween: 16,
        slidesPerGroup: 1,
        observer : true,
        observeParents: true,
        observeSlideChildren: true,
        loop: false,
        loopFillGroupWithBlank: true,
        breakpointsInverse: true,
        breakpoints: {
            0 :    { slidesPerView: 2, slidesPerGroup: 1, },
            640 :  { slidesPerView: 3, slidesPerGroup: 1, },
            1120 : { slidesPerView: 4, slidesPerGroup: 1, },
            1340 : { slidesPerView: 5, slidesPerGroup: 1, },
        },
        navigation: { 
            nextEl: '.watchlist_products_next', 
            prevEl: '.watchlist_products_prev', 
        },
    });
}




function watchlist() {
    let url = urls['watchlist']
    if (typeof setWatchList !== 'undefined') {
        url = setWatchList
    } 
    
    let csrf = Cookies.get()
    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("X-CSRFToken", csrf["csrftoken"]);
    request.send()
    request.onload = function () {
        let data = JSON.parse(request.responseText);
        let list = document.getElementById('watchlist-products')
        let template = document.getElementById('tpl_watchlist_product')

        list.innerHTML = nunjucks.renderString(template.innerHTML, data)
        WarchlistSwiper()
    }
} watchlist()
