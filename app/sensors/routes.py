from app.sensors.dht11 import DHT11
from app.sensors.distance_sensor import start_distance_measurement, set_process_run
from app import app, socketio
from flask import Response
from time import time
import threading

dht11 = DHT11()


@app.route('/dht11/start')
def dht11_start():
    dht11.start()
    return Response(200)


@app.route('/dht11/stop')
def dht11_stop():
    dht11.stop()
    return Response(200)


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


def thread_func():
    while(1):
        time.sleep(1)
        socketio.emit('my response', {'data': 'ddd'}, namespace='/test', room="room1")


x = threading.Thread(target=thread_func)