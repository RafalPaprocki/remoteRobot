from app.sensors.dht11 import DHT11
from app.sensors.distance_sensor import DistanceSensor
from app import app
from flask import Response, jsonify

dht11 = DHT11()
distance_sensor = DistanceSensor()


@app.route('/dht11/start')
def dht11_start():
    dht11.start()
    return Response(status=200)


@app.route('/dht11/stop')
def dht11_stop():
    dht11.stop()
    return Response(status=200)


@app.route('/distance_measurement/start')
def distance_measurement_start():
    distance_sensor.start()
    return Response(status=200)


@app.route('/distance_measurement/stop')
def distance_measurement_stop():
    distance_sensor.stop()
    return Response(status=200)


@app.route('/dht11/measure-weather', methods=['GET'])
def measure_temp():
    humidity, temperature = dht11.take_temp_and_humidity()
    return jsonify({"humidity": humidity, "temperature": temperature})

