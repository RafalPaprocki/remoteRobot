import RPi.GPIO as GPIO

class GPIO_config():
    LEFT_FRONT_MOTOR = 5
    LEFT_REAR_MOTOR = 26
    RIGHT_FRONT_MOTOR = 13
    RIGHT_REAR_MOTOR = 6
    GPIO_DHT = 4
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
    HORIZONTAL_SERV0 = 4
    VERTICAL_SERVO = 3

    @staticmethod
    def init_GPIO():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_config.LEFT_FRONT_MOTOR, GPIO.OUT)
        GPIO.setup(GPIO_config.LEFT_REAR_MOTOR, GPIO.OUT)
        GPIO.setup(GPIO_config.RIGHT_FRONT_MOTOR, GPIO.OUT)
        GPIO.setup(GPIO_config.RIGHT_REAR_MOTOR, GPIO.OUT)


