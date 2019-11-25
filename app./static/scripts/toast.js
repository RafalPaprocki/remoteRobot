function generateToast(toast_id) {
  var x = document.getElementById(toast_id);
  x.className = "toastr show-toast";
  setTimeout(function(){ x.className = x.className.replace("show-toast", ""); }, 3000);
}
