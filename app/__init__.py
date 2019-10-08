from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


socketio = SocketIO(app, async_mode="threading")

from app import routes
from app.robot_control import routes
from app.models import weather, route
