document.onkeydown = checkKey;
document.onkeyup = releaseKey;

var leftArrow = false
var rightArrow = false
var upArrow = false
var downArrow = false
var verticalSlider;
var horizontalSlider;

document.addEventListener('DOMContentLoaded', function() {
   verticalSlider = $("#verRange")[0]
   horizontalSlider = $("#horRange")[0]
}, false);

function checkKey(event) {
    if(event.defaultPrevented){
        return;
    }
    var key =  event.key || event.keyCode;
    if(key == "ArrowUp" || key == '38') {
        if(upArrow){
        }else{
            upArrow = true;
            changeCarMove();
        }
    }
    else if (key == "ArrowDown" || key == '40') {
        if(downArrow){
        }else{
            downArrow = true;
            changeCarMove();
        }
    }
    else if (key == 'ArrowLeft' || key == '37') {
        if(leftArrow){
        }else{
            leftArrow = true;
            changeCarMove();
        }
    }
    else if (key == 'ArrowRight' || key == '39') {
        if(rightArrow){
        }else{
            rightArrow = true;
            changeCarMove();
        }
    }
    else if (key == 'q' || key == 'Q' || key == '81') {
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/stop", true);
        xhttp.send();
    } else if (key == 'a' || key == 'A' || key == '65') {
        var xhttp = new XMLHttpRequest();
        let angle = parseInt(horizontalSlider.value)
        if(angle > 0) {
            angle -= 3;
            xhttp.open("GET", "robot/horizontal/move/" + angle, true);
            xhttp.send();
            horizontalSlider.value = angle
        }
    } else if (key == 'd' || key == 'D' || key == '68') {
        var xhttp = new XMLHttpRequest();
        let angle = parseInt(horizontalSlider.value)
        if(angle < 180) {
            angle += 3;
            xhttp.open("GET", "robot/horizontal/move/" + angle, true);
            xhttp.send();
            horizontalSlider.value = angle
        }
    } else if (key == 'w' || key == 'W' || key == '87') {
        var xhttp = new XMLHttpRequest();
        let angle = parseInt(verticalSlider.value)
        if(angle < 180) {
            angle += 3;
            xhttp.open("GET", "robot/vertical/move/" + angle, true);
            xhttp.send();
            verticalSlider.value = angle

        }
    } else if (key == 's' || key == 'S' || key == '83') {
        var xhttp = new XMLHttpRequest();
        let angle = parseInt(verticalSlider.value)
        if(angle > 0) {
            angle -= 3;
            xhttp.open("GET", "robot/vertical/move/" + angle, true);
            xhttp.send();
            verticalSlider.value = angle
        }
    }
}

function releaseKey(event) {
    if(event.defaultPrevented){
        return;
    }
    var key =  event.key || event.keyCode;
    if(key == "ArrowUp" || key == '38') {
        upArrow = false;
        console.log("upArrow false")
        changeCarMove();
    }
    else if (key == "ArrowDown" || key == '40') {
        downArrow = false;
        changeCarMove()
    }
    else if (key == 'ArrowLeft' || key == '37') {
        leftArrow = false;
        changeCarMove()
    }
    else if (key == 'ArrowRight' || key == '39') {
        rightArrow = false;
        changeCarMove()
    }
}

function changeCarMove() {
    if(upArrow && leftArrow && !downArrow && !rightArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/left_forward", true);
        xhttp.send();
    }else if(upArrow && rightArrow && !downArrow && !leftArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/right_forward", true);
        xhttp.send();
    }else if(downArrow && rightArrow && !upArrow && !leftArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/right_back", true);
        xhttp.send();
    }else if(downArrow && leftArrow && !upArrow && !rightArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/left_back", true);
        xhttp.send();
    }else if(upArrow && rightArrow && !downArrow && !leftArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/right_forward", true);
        xhttp.send();
    }else if(upArrow && !rightArrow && !downArrow && !leftArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/forward", true);
        xhttp.send();
    }else if(downArrow && !rightArrow && !leftArrow && !leftArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/back", true);
        xhttp.send();
    }else if(rightArrow && !upArrow && !downArrow && !leftArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/right", true);
        xhttp.send();
    }else if(leftArrow && !rightArrow && !downArrow && !upArrow){
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/left", true);
        xhttp.send();
    }else {
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "robot/stop", true);
        xhttp.send();
    }
}

