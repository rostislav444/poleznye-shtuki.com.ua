var equipmentImage = document.getElementById('equipment_image_blocks')
var n = 50

if (equipmentImage != undefined) {
    for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= n; j++) {
        let eq = document.createElement('div')
        eq.id = 'eq' + j + '_' + i
        equipmentImage.appendChild(eq)
    }
}

const equipmentList = document.querySelector('.equipment__list').querySelectorAll('input')

var tippiDivs = []

for (let eq of equipmentList) {
    let div = document.getElementById(eq.dataset.id)    
    div.classList.add('doted')
    div.dataset.tippyContent = eq.dataset.text
   

    let tippyDiv = tippy(div, {
        trigger: 'click',
        placement : "bottom",
        // hideOnClick: 'toggle',
    })
    tippiDivs.push(tippyDiv)


    eq.addEventListener('change', function() {
        let dots = document.querySelectorAll('.doted')
        for (let dot of dots) { dot.classList.remove('hovered') }
        for (let tipp of tippiDivs) { tipp.hide() }


        if (eq.checked) { 
            div.classList.add('hovered') 
            tippyDiv.show()
        } 
    })
}
// tippy('[data-tippy-content]');
}