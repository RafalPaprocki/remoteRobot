from app import db
from datetime import datetime


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String)
    path = db.Column(db.String)
    preview_frame = db.Column(db.String)

    def __repr__(self):
        return '<Video {}>'.format(self.id)


