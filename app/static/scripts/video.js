let recording = false;
let loading = false;

let stop_recording_btn;
let start_recording_btn;
let fname_input;

document.addEventListener('DOMContentLoaded', function() {
    recording = sessionStorage.getItem("recording")
    stop_recording_btn = document.getElementById("stop_recording");
    start_recording_btn = document.getElementById("start_recording");
    fname_input = document.getElementById("fname");

    if(recording == "True") {
        stop_recording_btn.disabled = false;
        start_recording_btn.disabled = true;
        fname_input.disabled = true;
    }else{
        stop_recording_btn.disabled = true;
        start_recording_btn.disabled = true;
        fname_input.disabled = false;
    }
}, false);

function playVideo(videoName) {
    console.log(videoName)
  // var source = document.getElementById("asd").src = '/file-download/' + videoName ;
  // source.setAttribute('src', '/file-download/youroutput.mp4');
  // var video = document.getElementById('vid').load();
    document.getElementById("mp4_src").src = "file-download/youroutput.mp4";
    document.getElementById("myVideo").load();
}


function save() {
    recording = false
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/video/recording/stop", true);
    xhttp.onreadystatechange = function (){
        sessionStorage.removeItem('recording');
        start_recording_btn.disabled = true;
        stop_recording_btn.disabled = true;
        fname_input.value = ""
        fname_input.disabled = false
        generateToast("snackbar2")
    }
    xhttp.send()

    $('#exampleModalCenter').modal('hide')
}

function record(){
    let fname = document.getElementById('fname').value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/video/recording/start/" + fname, true);
    xhttp.onreadystatechange = function (){
        sessionStorage.setItem('recording', 'True');
        start_recording_btn.disabled = true;
        stop_recording_btn.disabled = false;
        fname_input.disabled = true;
        generateToast("snackbar")
    }

    xhttp.send();
    postVideo(fname)
    $('#exampleModalCenter').modal('hide')

}

function fnameUpdate(text) {
  if(text == undefined || text == ""){
      start_recording_btn.disabled = true;
  }else{
      start_recording_btn.disabled = false;
  }
}

function postVideo(fname){
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        xmlhttp.open("POST", "/video");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(JSON.stringify({videoname:fname, }));
}

