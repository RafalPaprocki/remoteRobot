from app import db
from datetime import datetime
from time import time


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    element = db.relationship('RouteElement', backref='route', lazy='dynamic')

    def __repr__(self):
        return '<Route {}>'.format(self.name)


class RouteElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    kind_id = db.Column(db.Integer, db.ForeignKey('element_kind.id'))
    duration = db.Column(db.Integer)
    angle = db.Column(db.Integer)

    def __repr__(self):
        return '<RouteElement {}>'.format(self.id)


class ElementKind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    route_element = db.relationship('RouteElement', backref='kind', lazy='dynamic')