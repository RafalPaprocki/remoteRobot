function toggleSidebar(){
    document.getElementById('sidebar').classList.toggle('active')
    document.getElementsByClassName('content')[0].classList.toggle('active')
}

function loadDatePicker(id, config){
    $('#'+id).datepicker(config);
}