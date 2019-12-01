import Adafruit_DHT
import time
from threading import Thread

from datetime import date, datetime, timedelta

from app.models.weather import Weather
from app import db

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
PAUSE_PERIOD = 60 # in minutes


class DHT11:
    def __init__(self):
        self.stopped = False

    @staticmethod
    def take_temp_and_humidity():
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        while humidity is None or temperature is None:
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        return humidity, temperature

    def start(self):
        self.stopped = False
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        d = datetime.today()
        if d.minute != 0:
            d1 = d.replace(minute=0, second=0) + timedelta(hours=1)
            time_to_wait = (d1-d).total_seconds()
            print(time_to_wait)
            time.sleep(time_to_wait)

        while True:
            h, t = DHT11.take_temp_and_humidity()
            w = Weather(humidity=h, temperature=t, date=datetime.today())
            db.session.add(w)
            db.session.commit()
            time.sleep(PAUSE_PERIOD * 60)
            print(t)
            if self.stopped:
                return

    def stop(self):
        self.stopped = True