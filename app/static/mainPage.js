function activeStop(){
    document.getElementById("stop").classList.toggle("active");
}

function distanceSensorStart(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/distance_measurement/start", true);
    xhttp.send();
}

function distanceSensorStop(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/distance_measurement/stop", true);
    xhttp.send();
}