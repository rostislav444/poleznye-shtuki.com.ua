var inValidFields = 0
    function AddMessage(input) {
        input.classList.remove('valid')
        input.classList.add('in_valid')

        let parent = input.parentNode
        let span = parent.querySelector("span.message")
        
        if (span == undefined) {
            span = document.createElement('span')
            span.classList.add('message')
        }
        span.innerHTML = ""
        span.innerHTML += " " + input.dataset.alert
        parent.insertBefore(span, input)
    }

    function ClearInput(input) {
        input.classList.add('valid')
        input.classList.remove('in_valid')
        let parent = input.parentNode
        let span = parent.querySelector("span.message")
        if (span != undefined) {
            span.remove()
        }

    }


    function Validate(input) {
        if (input.required == true && input.value.length == 0) {
            input.dataset.valid = false
        } else if (input.dataset.type == "phone") {
            let value = input.value.replace(/\D/g,'');
            if (value.length < 12) {
                input.dataset.valid = false
            }
        } 


        if (input.dataset.valid == "true") {
            ClearInput(input)
        } else {
            inValidFields += 1
            AddMessage(input)
        }
    }

    function SubmitForm(form) {
        form.submit()
    }


    var orderForm = document.getElementById("order__form")
    orderForm.addEventListener('submit', event => {
        inValidFields = 0
        for (let input of orderForm.querySelectorAll('input')) {
            if (input.required == true && input.value.length == 0) {
                input.dataset.valid = false
            } else {
                input.dataset.valid = true
            }
            Validate(input)
        }
        if (inValidFields == 0) {
            SubmitForm(orderForm)
        }
        event.preventDefault();
    });