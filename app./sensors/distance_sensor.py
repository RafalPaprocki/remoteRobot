# Libraries
import RPi.GPIO as GPIO
import time
from app import socketio
from threading import Thread
from app.hardware.GPIOConfig import  GPIO_config
GPIO.setmode(GPIO.BCM)
from app.robot_control.robot_control import withdraw

class DistanceSensor:
    def __init__(self):
        self.stopped = False
        GPIO.setup(GPIO_config.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_config.GPIO_ECHO, GPIO.IN)

    def start(self):
        self.stopped = False
        Thread(target=self.start_distance_measurement(), args=()).start()
        return self

    def stop(self):
        self.stopped = True

    def distance(self):
        GPIO.output(GPIO_config.GPIO_TRIGGER, True)

        time.sleep(0.00001)
        GPIO.output(GPIO_config.GPIO_TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(GPIO_config.GPIO_ECHO) == 0:
            start_time = time.time()

        while GPIO.input(GPIO_config.GPIO_ECHO) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2

        return distance

    def start_distance_measurement(self):
        try:
            while True:
                dist = self.distance()
                if dist < 12:
                    withdraw()
                time.sleep(0.1)
                if self.stopped:
                    break
                print(dist)
        except KeyboardInterrupt:
            GPIO.cleanup()
