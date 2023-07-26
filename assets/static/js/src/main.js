let goTop = document.querySelector('.go-top');

window.onscroll = () =>  {
    if (document.body.scrollTop > 1000 || document.documentElement.scrollTop > 1000) {
        goTop.style.display = "block";
    } else {
        goTop.style.display = "none";
    }
}

goTop.onclick = () => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}



