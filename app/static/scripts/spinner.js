function startLoading(){
    document.getElementsByClassName("main-container")[0].disabled = true;
    document.getElementsByClassName("main-container")[0].style.opacity = 0.8;
    document.getElementById("spinner").style.visibility = "visible"
}

function stopLoading(){
    document.getElementsByClassName("main-container")[0].disabled = false;
    document.getElementsByClassName("main-container")[0].style.opacity = 1;
    document.getElementById("spinner").style.visibility = "hidden"
}