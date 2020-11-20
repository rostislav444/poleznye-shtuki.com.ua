


// COMMENT FORM
let commentForm = document.getElementById("comment_form_form");
let comments = document.querySelector('.comments')
commentForm.addEventListener('submit', function(event) {
    event.preventDefault();
    method = commentForm.method
    url = commentForm.action
    enctype = commentForm.enctype
    data = new FormData(commentForm);
    
    boundary = Cookies.get()

    let msgBlock = commentForm.querySelector('.msg_block')

    let request = returnReuestXHR(method, url, data)
        request.onload = () => {
        if (request.status == 200) {
            let response = JSON.parse(request.responseText);
            if ('msg' in response) {
                msgBlock.querySelector('p').innerHTML = response['msg']
                msgBlock.classList.add('active')
            } else {
                msgBlock.classList.remove('active')
                $('.modaal').modaal('close');
                document.location.reload(true)
                
            }
            
            
            
        } else {
            alert('Ошибка: ' + request.status)
        }
    };
        

}, false);

function validatePhone(phone) {
    phone = phone.replace(/[^0-9.]/g, '');
    var re = /^[\d-]{7,9}$/
    return re.test(phone);
}

function validateEmail(email) {
     var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
     return re.test(email);
}






var usernameInput = document.getElementById('comment-form__username');
    usernameInput.onchange = () => {
        field = usernameInput.value
        if(!validateEmail(field) && !validatePhone(field)) {
            alert('Введите корректно Email или номер телефона')  
            return false;
        }
    }
   
   






// COMMENT PHONE MASK
// var element = document.getElementById('comment-form__username');
// var maskOptions = {
//         mask: '+{38}(000)000-00-00'
// };
// var mask = IMask(element, maskOptions);


// COMMENT CHOOSE STARS
let star_0 = '/static/img/ico/star-0.png'
let star_1 = '/static/img/ico/star-10.png'
let rateStars = document.querySelector('.rate_stars')
let stars = rateStars.querySelectorAll('.rate_star')
stars.forEach(star => {
    star.style.backgroundImage = 'url(' + star_1 + ')'
});

function SetStarIndex(index) {
    for (let i = 0; i < stars.length; i++) {
        let star = stars[i]
        if (i <= index) {
            star.style.backgroundImage = 'url(' + star_1 + ')'
        } else {
            star.style.backgroundImage = 'url(' + star_0 + ')'
        }
    }
}

for (let i = 0; i < stars.length; i++) {
    let el = stars[i];
    // MOUSEOVER
    el.addEventListener('mouseover', function() {
        SetStarIndex(i)
    })
    // CLICK
    el.addEventListener('click', function() {
        SetStarIndex(i)
        document.querySelector('input[name=stars]').value = i + 1
        // rateStars.dataset.rate = i+1
    })
}
rateStars.addEventListener('mouseout', function() {
    SetStarIndex(parseInt(document.querySelector('input[name=stars]').value) - 1)
})



