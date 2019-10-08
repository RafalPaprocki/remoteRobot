import Adafruit_DHT
import time
from threading import Thread
from app.models.weather import Weather
from app import db

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
PAUSE_PERIOD = 0.1 # in minutes


class DHT11:
    def __init__(self):
        self.stopped = False

    @staticmethod
    def take_temp_and_humidity():
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        return humidity, temperature

    def start(self):
        self.stopped = False
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            h, t = DHT11.take_temp_and_humidity()
            print(str(h))
            if h is not None and t is not None:
                w = Weather(humidity=h, temperature=t)
                db.session.add(w)
                db.session.commit()
                time.sleep(PAUSE_PERIOD * 60)
            if self.stopped:
                return

    def stop(self):
        self.stopped = True