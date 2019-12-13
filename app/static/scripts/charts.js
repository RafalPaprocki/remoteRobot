var chart;
var chart2;
var chart3;

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    let config = createConfig()
    chart = new Chart(ctx, config);

    var ctx2 = document.getElementById('canvas2').getContext('2d');
    let config2 = createConfig2("Dzienna temperatura dla wybranego miesiąca", "canvas2")
    chart2 = new Chart(ctx2, config2);

    var ctx3 = document.getElementById('canvas3').getContext('2d');
    let config3 = createConfig2("Miesięczna temperatura dla wybranego roku", "canvas3")
    chart3 = new Chart(ctx3, config3)

    loadDatePicker("date1", {autoHide: 'true',  format: 'dd.mm.YYYY'})
    $('#date1').on('pick.datepicker', function (e) {
        date = new Date(e.date);
        day = date.getDate();
        month = date.getMonth();
        year = date.getFullYear();
        getWeatherForDay(day, month, year)
        console.log("picked date")

    });
    $('#date1').datepicker('setDate', new Date());

    loadDatePicker("date2", {autoHide: 'true',  format: 'mm.YYYY'})
    $('#date2').on('pick.datepicker', function (e) {
        date = new Date(e.date);
        month = date.getMonth();
        year = date.getFullYear();
        getWeatherForMonth(month, year)
    });
    $('#date2').datepicker('setDate', new Date());

    loadDatePicker("date3", {autoHide: 'true',  format: 'YYYY'})
    $('#date3').on('pick.datepicker', function (e) {
        date = new Date(e.date);
        month = date.getMonth();
        year = date.getFullYear();
        getWeatherForYear(year)

    });
     $('#date3').datepicker('setDate', new Date());
     getWeatherForMonth(month, year)
}, false);


function createConfig(){
    labels=['0']
    data=[1]
    var config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Wilgotność',
                fill: false,
                backgroundColor: '#0000FF',
                borderColor: '#0000FF',
                data: data,
            }, {
                label: 'Temperatura',
                fill: true,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'rgba(75, 192, 192,1)',
                borderDash: [1, 1],
                data: data
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Temperatura godzinowa dla podanego dnia'
            },
            animation: {
            onComplete: function() {
                    stopLoading("spinner-day", "canvas")
                    console.log("stopped")
                }
            },
            tooltips: {
                mode: 'index',
                intersect: false,
                filter: function(x) {return x.yLabel != 0.001}
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                x: {
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Month'
                    }
                },
                y: {
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                },
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                    }
                }],
            }
        }
    };
    return config;
}

function createConfig2(chart_title, canvasId=''){
    var config = {
        type: 'bar',
        data: {
        labels: [],
        datasets: [{
            label: 'Wilgotność',
            backgroundColor: '#0000FF',
            borderColor: '#0000FF',
            borderWidth: 1,
            data: []
        }, {
            label: 'Temperatura',
            backgroundColor: 'rgba(75, 192, 192, 0.7)',
            borderColor: 'rgba(75, 192, 192, 0.7)',
            borderWidth: 1,
            data: []
        }]
		},
        options: {
            responsive: true,
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: chart_title
            },
             animation: {
                onComplete: function() {
                    if(canvasId == 'canvas3'){
                        stopLoading("spinner-year", canvasId)
                        console.log("stopped")
                    }
                    if(canvasId == 'canvas2'){
                         stopLoading("spinner-month", canvasId)
                        console.log("stopped")
                    }

                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                    }
                }],
            }
        }
    };
    return config;
}

function getWeatherForDay(day=1,month=1,year=2017) {
    var xhttp = new XMLHttpRequest();
    startLoading("spinner-day", "canvas")
    xhttp.open("GET", `/take/${day}/${month}/${year}`, true);
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            var weather = JSON.parse(this.responseText);
            console.log(weather)
            chart.data.datasets[0].data = weather.humidity;
            chart.data.datasets[1].data = weather.temperature;
            chart.data.labels = weather.labels;
            chart.update()
        }
    }
    xhttp.send();

}

function getWeatherForMonth(month=1, year=2017){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", `/takea/${month}/${year}`, true);
    startLoading("spinner-month", "canvas2")
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            var weather = JSON.parse(this.responseText);
            console.log(weather)
            chart2.data.datasets[0].data = weather.humidity;
            chart2.data.datasets[1].data = weather.temperature;
            chart2.data.labels = weather.labels;
            chart2.update()
        }
    }
    xhttp.send();
}

function getWeatherForYear(year=2019){
    var xhttp = new XMLHttpRequest();
    startLoading("spinner-year", "canvas3")
    xhttp.open("GET", `/takea/${year}`, true);
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            var weather = JSON.parse(this.responseText);
            console.log(weather)
            chart3.data.datasets[0].data = weather.humidity;
            chart3.data.datasets[1].data = weather.temperature;
            chart3.data.labels = weather.labels;
            chart3.update()

        }
    }
    xhttp.send();
}
