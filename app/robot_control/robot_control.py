import RPi.GPIO as GPIO
from app.hardware.GPIOConfig import GPIO_config


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
