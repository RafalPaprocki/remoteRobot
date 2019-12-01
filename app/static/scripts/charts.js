document.addEventListener('DOMContentLoaded', function() {
    loadDatePicker("date1", {autoHide: 'true',  format: 'dd.mm.YYYY'})
    $('#date1').on('pick.datepicker', function (e) {
        date = new Date(e.date);
        day = date.getDate();
        month = date.getMonth();
        year = date.getFullYear();
        getWeatherForDay(day, month, year)
    });
    loadDatePicker("date2", {autoHide: 'true',  format: 'mm.YYYY'})
    $('#date2').on('pick.datepicker', function (e) {
        date = new Date(e.date);
        month = date.getMonth();
        year = date.getFullYear();
        getWeatherForMonth(month, year)
    });
    loadDatePicker("date3", {autoHide: 'true',  format: 'YYYY'})
    $('#date3').on('pick.datepicker', function (e) {
        date = new Date(e.date);
        month = date.getMonth();
        year = date.getFullYear();
        getWeatherForYear(year)
    });
}, false);


function createConfig(labels, temperatureData, humidityData){
    var config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Wilgotność',
                fill: false,
                backgroundColor: '#0000FF',
                borderColor: '#0000FF',
                data: humidityData,
            }, {
                label: 'Temperatura',
                fill: true,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'rgba(75, 192, 192,1)',
                borderDash: [1, 1],
                data: temperatureData
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Chart.js Line Chart'
            },
            animation: {
            onComplete: function() {

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

function createConfig2(){
    var config = {
        type: 'bar',
				data: {
			labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April', 'May', 'June'],
			datasets: [{
				label: 'Dataset 1',
				backgroundColor: 'rgba(75, 192, 192, 0.7)',
				borderColor: 'rgba(75, 192, 192, 0.7)',
				borderWidth: 1,
				data: [
					'34',
					'35',
					'36',
					'37',
					'1',
					'3',
					'3',
					'12',
					'24',
					'26',
					'28',
					'29',
					'30',
				]
			}, {
				label: 'Dataset 2',
				backgroundColor: '#0000FF',
				borderColor: '#0000FF',
				borderWidth: 1,
				data: [
					'12',
                    '25',
					'26',
					'27',
					'1',
					'3',
					'3',
					'32',
					'34',
					'36',
					'18',
					'19',
					'10',

				]
			}]
		},
				options: {
					responsive: true,
					legend: {
						position: 'top',
					},
					title: {
						display: true,
						text: 'Chart.js Bar Chart'
					}
				}
    };
    return config;
}


var chart;
var chart2;
var chart3;
let datas = [2, 1, 5, 3, 6]
let labels = ["00:00", "01:00", "02:00", "03:00", "04:00"]
window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    let config = createConfig(labels, datas, datas)
    chart = new Chart(ctx, config);

    var ctx2 = document.getElementById('canvas1').getContext('2d');
    let config2 = createConfig2()
    chart2 = new Chart(ctx2, config2);

    var ctx3 = document.getElementById('canvas3').getContext('2d');
    let config3 = createConfig2()
    chart3 = new Chart(ctx3, config3)



};

function getWeatherForDay(day=1,month=1,year=2017) {
    var xhttp = new XMLHttpRequest();
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
function change(){
    getWeatherForDay()

}