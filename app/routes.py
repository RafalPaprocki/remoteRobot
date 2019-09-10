from flask import render_template, flash, redirect, url_for, request
from flask import Response
from app import app, socketio
from app.camera_pi import Camera
from app.preprocessing import Processing
from flask_socketio import emit, join_room, leave_room
import threading
import time
from app.hardware.distance_sensor import start_distance_measurement, set_process_run
import cv2

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
    p = Processing()
    # p.load()
    camera = Camera()
    camera.initialize()
    i = 0
    while True:
            frame = camera.take_frame()
            frame = Processing.to_np_array(frame)
            # frame = p.image_preprocess(frame)
            i += 1
            frame = Processing.to_jpeg(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_stream')
def video_stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/distance_measurement/start')
def distance_measurement_start():
    set_process_run(True)
    a = threading.Thread(target=start_distance_measurement())
    a.start()
    return Response(200)


@app.route('/distance_measurement/stop')
def distance_measurement_stop():
    set_process_run(False)
    return Response(200)


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})
    print(clients)



@socketio.on('my broadcast event', namespace='/test')
def test_messagee(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('join', namespace='/test')
def join_roome(data):
    room = "room1"
    join_room(room)
    x.start()


@socketio.on('leave', namespace="/test")
def leave_roome(data):
    room = "room1"
    leave_room(room)


clients = []


@socketio.on('connect', namespace='/test')
def connect():
    clients.append(request.remote_user)


@socketio.on('disconnect', namespace='/test')
def disconnect():
    clients.remove(request.remote_user)


def thread_func():
    while(1):
        time.sleep(1)
        socketio.emit('my response', {'data': 'ddd'}, namespace='/test', room="room1")


x = threading.Thread(target=thread_func)