function startLoading(spinnerId, disabledId){
    document.getElementById(disabledId).disabled = true;
    document.getElementById(disabledId).style.opacity = 0.7;
    document.getElementById(spinnerId).style.visibility = "visible"
}

function stopLoading(spinnerId, disabledId){
    document.getElementById(disabledId).disabled = false;
    document.getElementById(disabledId).style.opacity = 1;
    document.getElementById(spinnerId).style.visibility = "hidden"
}