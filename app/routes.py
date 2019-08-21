from flask import render_template, flash, redirect, url_for, request
from flask import Response
from app import app
from app.camera_pi import Camera


@app.route('/')
def index():
    return render_template('mainPage.html')


@app.route('/robot-config')
def robot_config():
    return render_template('robotConfig.html')


@app.route('/robot-routes')
def robot_routes():
    return render_template('robotRoutes.html')


@app.route('/data-preview')
def data_preview():
    return render_template('dataPreview.html')


def gen():
    camera = Camera()
    camera.initialize()
    while True:
            frame = camera.take_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_stream')
def video_stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')