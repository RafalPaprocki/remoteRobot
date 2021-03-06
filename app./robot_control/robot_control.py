import RPi.GPIO as GPIO
from app.hardware.GPIOConfig import GPIO_config
import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)


def forward():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.HIGH)


def left():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.LOW)


def right():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.HIGH)


def back():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.LOW)


def stop():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.LOW)


def left_forward():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.LOW)


def right_forward():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.HIGH)


def left_back():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.LOW)


def right_back():
    GPIO.output(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.RIGHT_REAR_MOTOR, GPIO.LOW)
    GPIO.output(GPIO_config.LEFT_FRONT_MOTOR, GPIO.HIGH)
    GPIO.output(GPIO_config.LEFT_REAR_MOTOR, GPIO.LOW)

def withdraw():
    back()
    time.sleep(0.5)
    stop()

def servo_move(servo_number, angle):
    kit.servo[servo_number].angle = int(angle)


def steering_with_angle(steering_angle, lane_lines):
    if len(lane_lines) > 1:
        if steering_angle < 70:
            left_forward()
            time.sleep(0.1)
            stop()
        elif steering_angle < 115:
            forward()
            time.sleep(0.1)
            stop()
        elif steering_angle < 170:
            right_forward()
            time.sleep(0.1)
            stop()
        else:
            stop()

    if len(lane_lines) == 1:
        x1, y1, x2, y2 = lane_lines[0][0]
        print("x1: " + str(x1))

        if x1 < 580:
            left_forward()
            time.sleep(0.1)
            stop()

        else:
            forward()
            time.sleep(0.1)
            stop()

    if len(lane_lines) == 0 or lane_lines is None:
        stop()
