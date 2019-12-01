let measuring = false;
let startMeasuringRadio;
let stopMeasuringRadio;

document.addEventListener('DOMContentLoaded', function() {
    measuring = sessionStorage.getItem("measuring")
    stopMeasuringRadio = document.getElementById("stopRadio");
    startMeasuringRadio = document.getElementById("startRadio");

    if(measuring == "True") {
        startMeasuringRadio.disabled = true;
        stopMeasuringRadio.disabled = false;
    }else{
        startMeasuringRadio.disabled = false;
        stopMeasuringRadio.disabled = true;
    }
    hideWeatherInfo();
}, false);

function startMeasure(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/dht11/start", true);
    xhttp.onreadystatechange = function (){
        sessionStorage.setItem('measuring', 'True');
        stopMeasuringRadio.disabled = false;
        startMeasuringRadio.disabled = true;
        startMeasuringRadio.checked = false;
    }
    xhttp.send();
    hideWeatherInfo();
    $('#temperatureModal').modal('hide')
}

function stopMeasure(){
    var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "/dht11/stop", true);
        xhttp.onreadystatechange = function (){
            sessionStorage.removeItem('measuring');
            stopMeasuringRadio.disabled = true;
            startMeasuringRadio.disabled = false;
            stopMeasuringRadio.checked = false;
        }
        xhttp.send();
        hideWeatherInfo();
        $('#temperatureModal').modal('hide')
}

function oneTimeMeasure(){
    var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "/dht11/measure-weather", true);
        xhttp.onreadystatechange = function (){
            if (this.readyState == 4 && this.status == 200) {
                var weather = JSON.parse(this.responseText);
                showWeatherInfo(weather.temperature, weather.humidity);
                console.log(weather)
            }
            stopLoading();
        }
        xhttp.send();
        startLoading();
}

function doAction(){
    var radios = document.getElementsByName('radio');
    let checkedRadio = null;
    radios.forEach((r) => {
        if(r.checked){
            checkedRadio = r;
        }
    })
    if(checkedRadio != null){
        switch(checkedRadio.id){
            case "stopRadio":
                stopMeasure();
                break;
            case "startRadio":
                startMeasure();
                break;
            case "oneTimeRadio":
                oneTimeMeasure();
                break;
        }
    }
}

function showWeatherInfo(temperature, humidity) {
    $( "#weatherInfo" ).show(1000)
    document.getElementById('weatherInfo').innerHTML = `<div style="position:absolute; left:97%; top:-16%; cursor:pointer; " 
    onclick="hideWeatherInfo()">x</div>Temperatura = ${temperature}° , Wilgotność ${humidity}%`
    console.log("asd")
}

function hideWeatherInfo() {
    $("#weatherInfo").hide(1000);
}


