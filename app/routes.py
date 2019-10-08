from flask import render_template, request
from flask import Response
from app import app, socketio
from flask_socketio import emit, join_room, leave_room
import threading
import time
from app.hardware.distance_sensor import start_distance_measurement, set_process_run
from app.hardware.dht11 import DHT11



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