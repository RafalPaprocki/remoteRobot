var hidden = false;

$(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
});

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

function init() {
  var xCenter = 150;
  var yCenter = 150;
  var stage = new createjs.Stage('joystick');

  var psp = new createjs.Shape();
  psp.graphics.beginFill('#333333').drawCircle(xCenter, yCenter, 50);

  psp.alpha = 0.25;

  var vertical = new createjs.Shape();
  var horizontal = new createjs.Shape();
  vertical.graphics.beginFill('#ff3c42').drawRect(150, 0, 2, 300);
  horizontal.graphics.beginFill('#ff4d4d').drawRect(0, 150, 300, 2);

  stage.addChild(psp);
  stage.addChild(vertical);
  stage.addChild(horizontal);
  createjs.Ticker.framerate = 60;
  createjs.Ticker.addEventListener('tick', stage);
  stage.update();

  var myElement = $('#joystick')[0];

  var mc = new Hammer(myElement);

  mc.on("panstart", function(ev) {
    var pos = $('#joystick').position();
    xCenter = psp.x;
    yCenter = psp.y;
    psp.alpha = 0.5;

    stage.update();
  });

  mc.on("panmove", function(ev) {
    var pos = $('#joystick').position();

    var x = (ev.center.x - pos.left - 150);
    var y = (ev.center.y - pos.top - 150);

    var coords = calculateCoords(ev.angle, ev.distance);

    psp.x = coords.x;
    psp.y = coords.y;
     $('#xVal').text('X: ' + psp.x);
     $('#yVal').text('Y: ' + (-1 * psp.y));
    psp.alpha = 0.5;
    defineCarAction(psp.x, -1 * psp.y)
    stage.update();
  });

  mc.on("panend", function(ev) {
    psp.alpha = 0.25;
    createjs.Tween.get(psp).to({x:xCenter,y:yCenter},750,createjs.Ease.elasticOut);
    xhttp.open("GET", "robot/stop", true);
    xhttp.send();
  });
}

function calculateCoords(angle, distance) {
  var coords = {};
  distance = Math.min(distance, 100);
  var rads = (angle * Math.PI) / 180.0;

  coords.x = distance * Math.cos(rads);
  coords.y = distance * Math.sin(rads);

  return coords;
}

var xhttp = new XMLHttpRequest();

function defineCarAction(x, y) {
  if(x >= -11 && x<= 11 && y >= -100 && y <= -89){
    xhttp.open("GET", "robot/back", true);
    xhttp.send();
  }else if(x <= -66 && x >= -78 && y <= -62 && y >= -74){
    xhttp.open("GET", "robot/left_back", true);
    xhttp.send();
  }else if(x >= -100 && x <= -89 && y >= -11 && y <= 11){
    xhttp.open("GET", "robot/left", true);
    xhttp.send();
  }else if(x <= -66 && x >= -78 && y <= 74 && y >= 62){
    xhttp.open("GET", "robot/left_forward", true);
    xhttp.send();
  }else if(x >= -11 && x<= 11 && y >= 89 && y <= 100){
    xhttp.open("GET", "robot/forward", true);
    xhttp.send();
  }else if(x <= 78 && x >= 66 && y <= 74 && y >= 62){
    xhttp.open("GET", "robot/right_forward", true);
    xhttp.send();
  }else if(x >= 89 && x <= 100 && y >= -11 && y <= 11){
    xhttp.open("GET", "robot/right", true);
    xhttp.send();
  }else if(x <= 78 && x >= 66 && y <= -62 && y >= -74){
    xhttp.open("GET", "robot/right_back", true);
    xhttp.send();
  }else{
    xhttp.open("GET", "robot/stop", true);
    xhttp.send();

  }
}

function verticalCamera(value) {
  xhttp.open("GET", "robot/vertical/move/" + value, true);
  xhttp.send();
  console.log("vertical: " + value)

}

function horizontalCamera(value) {
  xhttp.open("GET", "robot/horizontal/move/" + value, true);
  xhttp.send();
  console.log("horizontal: " + value)
}

function hideControl() {
  if(hidden){
     $( ".control" ).show(1000)
    hidden = false
  }else {
    $(".control").hide(1000);
    hidden = true
  }
}

$(document).ready(function() {

});