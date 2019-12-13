from app import db
from datetime import datetime
from time import time


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.today())
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)

    def __repr__(self):
        return '<Weather {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'humidity': self.humidity,
            'temperature': self.temperature
        }
