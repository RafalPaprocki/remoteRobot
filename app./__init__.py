from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.hardware.GPIOConfig import GPIO_config


GPIO_config.init_GPIO()
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


socketio = SocketIO(app, async_mode="threading")

from app.robot_control import routes
from app.streaming import routes
from app.sensors import routes
from app.main import routes
from app.models import weather, route, video
