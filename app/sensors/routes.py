import datetime
from random import randrange

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.sensors.dht11 import DHT11
from app.sensors.distance_sensor import DistanceSensor
from app import app
from flask import Response, jsonify

from app.models.weather import Weather
from app import db
import sqlalchemy as sa
dht11 = DHT11()
distance_sensor = DistanceSensor()

MONTHS = {
    '1': "Styczen",
    '2': "Luty",
    '3': "Marzec",
    '4': "Kwiecien",
    '5': "Maj",
    '6': "Czerwiec",
    '7': "Lipiec",
    '8': "Sierpien",
    '9': "Wrzesien",
    '10': "Pazdziernik",
    '11': "Listopad",
    '12': "Grudzien",
}

@app.route('/dht11/start', methods=['GET'])
def dht11_start():
    dht11.start()
    return Response(status=200)


@app.route('/dht11/stop', methods=['GET'])
def dht11_stop():
    dht11.stop()
    return Response(status=200)


@app.route('/distance_measurement/start', methods=['GET'])
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

@app.route('/gen_data')
def gen_data():
    for i in range(0,24):
        temp_0_6 = randrange(9,15);
        temp_6_12 = randrange(14,18);
        temp_12_18 = randrange(18,24);
        temp_18_24 = randrange(16,20);

        hum_0_6 = randrange(50, 70);
        hum_6_12 = randrange(50, 60);
        hum_12_18 = randrange(37, 52);
        hum_18_24 = randrange(40, 52);

        if(i <= 6):
            w = Weather(date=datetime.datetime(2019,10,1, i, 0, 0), humidity=hum_0_6, temperature=temp_0_6)
        elif (i <= 12):
            w = Weather(date=datetime.datetime(2019, 10, 1, i, 0, 0), humidity=hum_6_12, temperature=temp_6_12)
        elif (i <= 18):
            w = Weather(date=datetime.datetime(2019, 10, 1, i, 0, 0), humidity=hum_12_18, temperature=temp_12_18)
        elif (i <= 24):
            w = Weather(date=datetime.datetime(2019, 10, 1, i, 0, 0), humidity=hum_18_24, temperature=temp_18_24)

        db.session.add(w)
    db.session.commit();
    return Response(status=200)


@app.route('/take/<day>/<month>/<year>', methods=['GET'])
def take_weather_day(day, month, year):
    todays_datetime_start = datetime.datetime(int(year), int(month)+1, int(day), 0,0,0)
    todays_datetime_end = datetime.datetime(int(year), int(month)+1, int(day), 23, 59, 59)
    weathers2 = Weather.query\
        .filter(Weather.date >= todays_datetime_start)\
        .filter(Weather.date <= todays_datetime_end).order_by(Weather.date).all()
    temperature_data = []
    humiditie_data = []
    labels = []
    if len(weathers2) > 0:
        first_hour = weathers2[0].date.hour
        last_hour = weathers2[-1].date.hour
        labels = []
        i = 0
        humiditie_data = []
        temperature_data = []
        print(last_hour)
        for a in range(first_hour, last_hour+1):
            labels.append(datetime.time(a).strftime("%H:%M"))
            if weathers2[i].date.hour == a:
                humiditie_data.append(weathers2[i].humidity)
                temperature_data.append(weathers2[i].temperature)
                i += 1
            else:
                temperature_data.append(None)
                humiditie_data.append(None)

            print(a)
    else:
        for a in range(0,24):
            labels.append(datetime.time(a).strftime("%H:%M"))

    return jsonify(weather=[w.serialize for w in weathers2],
                    labels=labels, temperature=temperature_data, humidity=humiditie_data)


@app.route('/takea/<month>/<year>', methods=['GET'])
def take_weather_month( month, year):
    todays_datetime_start = datetime.datetime(int(year), int(month)+1, 1, 0,0,0)
    todays_datetime_end = datetime.datetime(int(year), int(month)+1, 30, 23, 59, 59)
    weather3 = Weather.query\
        .with_entities(sa.func.avg(Weather.temperature).label('average'),
                       sa.func.avg(Weather.humidity).label('average'), Weather.date) \
        .filter(Weather.date >= todays_datetime_start) \
        .filter(Weather.date <= todays_datetime_end).order_by(Weather.date) \
        .group_by(sa.func.strftime("%Y-%m-%d", Weather.date))\
        .order_by(Weather.date)\
        .all()
    temperature_data = []
    humidity_data = []
    labels = []
    for data in weather3:
        temperature_data.append(data[0])
        humidity_data.append(data[1])
        labels.append(str(datetime.date(data[2].year, data[2].month, data[2].day)))
    if len(labels) == 0:
        for i in range(1,31):
            labels.append(str(datetime.date(int(year), int(month)+1, int(i))))
    return jsonify(weather=weather3, temperature=temperature_data, humidity=humidity_data, labels=labels)


@app.route('/takea/<year>', methods=['GET'])
def take_weather_year(year):
    todays_datetime_start = datetime.datetime(int(year), 1, 1, 0, 0, 0)
    todays_datetime_end = datetime.datetime(int(year), 12, 31, 23, 59, 59)
    weather = Weather.query\
        .with_entities(sa.func.avg(Weather.temperature).label('average'),
                       sa.func.avg(Weather.humidity).label('average'), Weather.date) \
        .filter(Weather.date >= todays_datetime_start) \
        .filter(Weather.date <= todays_datetime_end).order_by(Weather.date) \
        .group_by(sa.func.strftime("%Y-%m", Weather.date))\
        .order_by(Weather.date)\
        .all()
    temperature_data = []
    humidity_data = []
    labels = []
    for data in weather:
        temperature_data.append(data[0])
        humidity_data.append(data[1])
        labels.append(MONTHS[str(data[2].month)])
    if len(labels) == 0:
        for i in range(1, 13):
            labels.append(MONTHS[str(i)])

    return jsonify(weather=weather, temperature=temperature_data, humidity=humidity_data, labels=labels)