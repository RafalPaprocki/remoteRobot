function toggleSidebar(){
    console.log(document.getElementById('sidebar').classList.toggle('active'))
    console.log(document.getElementsByClassName('content')[0].classList.toggle('active'))
}