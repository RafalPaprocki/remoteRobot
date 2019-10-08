# Libraries
import RPi.GPIO as GPIO
import time
from app import socketio

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

process_run = False


def set_process_run(val):
    global process_run
    process_run = val


def distance():
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance


def start_distance_measurement():
    try:
        while True:
            dist = distance()
            if dist < 8:
                socketio.emit('warning response', {'data': dist}, namespace='/test')
            time.sleep(0.1)
            socketio.emit('my response', {'data': dist}, namespace='/test')
            if not process_run:
                break
    except KeyboardInterrupt:
        GPIO.cleanup()
