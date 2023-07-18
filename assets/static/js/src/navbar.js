let menu = document.querySelector(".navbar-menu")
let mobile = document.querySelector(".mobile")
let mobileIcons = mobile.querySelectorAll(".bi")
let links = document.querySelectorAll(".navigation a")
let currentLink = 1

mobile.addEventListener("click", (e)=> {
    e.preventDefault()
    let showMenu = menu.classList.toggle("show")
    if (showMenu) {
        mobileIcons[0].style.display = "none"
        mobileIcons[1].style.display = "block"
    } else {
        mobileIcons[0].style.display = "block"
        mobileIcons[1].style.display = "none"
    }
})


for (let i=0; i < links.length; i++) {
    let link = links[i]
    if (link.href == document.location.href) {
        currentLink = i
    }
}

links[currentLink].classList.add("active")

