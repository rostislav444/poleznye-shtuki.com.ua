function Close(id) {
    let conteiner = document.getElementById(id)
    conteiner.classList.remove('active')
}

function SimpleOpen(id) {
    let conteiner = document.getElementById(id)    
    conteiner.style.display = 'flex'
}

function Open(id, obj) {
    let conteiner = document.querySelector(id)
    if (obj.childNodes != undefined) {
        var childs = Array.prototype.slice.call(obj.childNodes)
    } else {
        var childs = []
    }
    

    function ChildsRecurion(obj) {
        if (obj.childNodes.length > 0) {
            Object.values(obj.childNodes).forEach(el => {
                childs.push(obj)
                ChildsRecurion(el)
            });
        } else {
            childs.push(obj)
        }
    }
       
    ChildsRecurion(obj)
    


    
    

    var listener = function (event) {
        
        let conteiner = document.querySelector(id)
        let isClickInside = conteiner.contains(event.target);
        if (isClickInside == false && childs.includes(event.target) == false) {
            conteiner.classList.remove('active')
            document.removeEventListener('click', listener, true);
        } 
    }  
    
    
    if (conteiner.classList.contains('active') == false) {
        conteiner.classList.add('active')
        document.addEventListener('click', listener, true)
    } else {
        conteiner.classList.remove('active')
        document.removeEventListener('click', listener, true);
    }
}

// while (el.parentNode) {
//     el = el.parentNode;
//     if (el.matches && el.matches(selector)) {
//         return el;
//     }
// }

