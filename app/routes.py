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
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from app.models.weather import Weather
from app.hardware.dht11 import DHT11

kit = ServoKit(channels=16)
dht11 = DHT11()


@app.route('/')
def index():
    return render_template('mainPage.html')


@app.route('/startt')
def startt():
    dht11.start()
    return "ok"


@app.route('/stop')
def stop():
    dht11.stop()
    return "ok"

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


@app.route("/robot/back", methods=['GET'])
def robot_back():
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    return "ok"


@app.route("/robot/forward", methods=['GET'])
def robot_forward():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    return "ok"


@app.route("/robot/left", methods=['GET'])
def robot_left():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    return "ok"


@app.route("/robot/right", methods=['GET'])
def robot_right():
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)

    return "ok"


@app.route("/robot/stop", methods=['GET'])
def robot_stop():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    return "ok"


@app.route("/robot/right_forward", methods=['GET'])
def robot_right_forward():
    r = Weather(humidity=34,temperature=21)
    print(r)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)

    return "ok"


@app.route("/robot/left_forward", methods=['GET'])
def robot_left_forward():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    return "ok"


@app.route("/robot/left_back", methods=['GET'])
def robot_left_back():
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    return "ok"


@app.route("/robot/right_back", methods=['GET'])
def robot_right_back():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    return "ok"


@app.route("/robot/horizontal/move/<angle>", methods=['GET'])
def robot_horizontal_move(angle):
    kit.servo[4].angle = int(angle)
    return "ok"


@app.route("/robot/vertical/move/<angle>", methods=['GET'])
def robot_vertical_move(angle):
    kit.servo[3].angle = int(angle)
    return "ok"


x = threading.Thread(target=thread_func)