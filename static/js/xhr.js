function XHR(method, url, data) {
    let csrf = Cookies.get()
    let request = new XMLHttpRequest();
        request.open(method, url, false);
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("X-CSRFToken", csrf["csrftoken"]);
        request.send(data)
        if (request.status == 200) {
             return JSON.parse(request.responseText);
        } else {
            alert('Ошибка: ' + request.status)
        }

}

function returnReuestXHR(method, url, data) {
    let csrf = Cookies.get()
    let request = new XMLHttpRequest();
        request.open(method, url, true);
        request.setRequestHeader("X-CSRFToken", csrf["csrftoken"]);
        request.send(data)
        return request
        if (request.status == 200) {
             return JSON.parse(request.responseText);
        } else {
            alert('Ошибка: ' + request.status)
        }

}