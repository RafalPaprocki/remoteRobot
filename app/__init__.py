from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode="threading")

from app import routes
