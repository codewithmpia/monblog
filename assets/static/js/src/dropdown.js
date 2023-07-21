let dropdown = document.querySelector(".dropdown")

if (dropdown) {
    dropdown.querySelector(".dropdown-btn").addEventListener("click", (e)=> {
        e.preventDefault()
        let dropdownItemsShow = dropdown.querySelector(".dropdown-items").classList.toggle("show")
        
        if (dropdownItemsShow) {
            dropdown.querySelector(".bi-chevron-down").classList.add("btn-svg-rotate")
            dropdown.querySelector(".bi-chevron-down").classList.remove("btn-svg-rotate-replace")
        } else {
            dropdown.querySelector(".bi-chevron-down").classList.replace("btn-svg-rotate", "btn-svg-rotate-replace")
        }
    })    
}