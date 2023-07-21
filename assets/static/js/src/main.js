let goTop = document.querySelector('.go-top');
let largeur = window.innerWidth 
let hauteur = window.innerHeight


window.onscroll = () =>  {
    if (document.body.scrollTop > 1000 || document.documentElement.scrollTop > 1000) {
        goTop.style.display = "block";
        if (largeur > 900) {
            goTop.style.right = `${(largeur - 900) / 2}px`;
        }
    } else {
        goTop.style.display = "none";
    }
}


goTop.onclick = () => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}



