from flask_sqlalchemy import SQLAlchemy
from app import app
from passlib.hash import sha512_crypt

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Aircraft(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(30), nullable=False)
    registration = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    icao = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(30), nullable=False)


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    designation = db.Column(db.String(8), nullable=False)
    return_flight = db.Column(db.String, db.ForeignKey('flight.id'), nullable=True)
    flight = db.relationship('FlightLeg', back_populates='flight', lazy=True, uselist=True)


# Used to define legs of flights
class FlightLeg(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    leg = db.Column(db.Integer, default=1)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    # These two don't need to exclude each other to allow for scenic routes that return to the same airport
    departure_airport = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    arrival_airport = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    hash = db.Column(db.String(160), nullable=False)

    def generate_hash(self, password):
        return sha512_crypt.hash(password)



def reset_db():
    db.drop_all(bind=None)
    db.create_all(bind=None)
    db.session.commit()
