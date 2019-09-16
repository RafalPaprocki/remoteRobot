from app import db
from datetime import datetime
from time import time


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)

    def __repr__(self):
        return '<Weather {}>'.format(self.id)

