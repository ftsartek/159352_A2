from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from app import app
from passlib.hash import sha512_crypt
import random

db = SQLAlchemy(app)

class Aircraft(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(30), nullable=False)
    registration = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    retired = db.Column(db.Boolean, nullable=False)
    maintenance_due = db.Column(db.Date, nullable=False)
    flights = db.relationship('Flight', backref='aircraft', lazy=True, uselist=True)


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    designation = db.Column(db.String(8), nullable=False)
    return_flight_id = db.Column(db.String, db.ForeignKey('flight.id'), nullable=True)
    aircraft_id = db.Column(db.String, db.ForeignKey('aircraft.id'), nullable=False)
    flight = db.relationship('FlightLeg', backref='flight', lazy=True, uselist=True)


# Used to define legs of flights
class FlightLeg(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    leg = db.Column(db.Integer, default=1)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    # These two don't need to exclude each other to allow for scenic routes that return to the same airport
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    icao = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    departures = db.relationship('FlightLeg', backref='departure_airport', lazy=True, uselist=True,
                                 foreign_keys=[FlightLeg.departure_airport_id])
    arrivals = db.relationship('FlightLeg', backref='arrival_airport', lazy=True, uselist=True,
                               foreign_keys=[FlightLeg.arrival_airport_id])


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tickets = db.relationship('Ticket', backref='booking', lazy=True, uselist=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    hash = db.Column(db.String(160), nullable=False)
    verification_code = db.Column(db.String(20), nullable=True)
    verified = db.Column(db.Boolean, nullable=False)
    disabled = db.Column(db.Boolean, nullable=False, default=False)
    bookings = db.relationship('Booking', backref='user', lazy=True, uselist=True)


    def generate_hash(self, password):
        return sha512_crypt.hash(password)

    def validate_account(self, code):
        if self.verification_code == code:
            self.verification_code = None
            return True
        else:
            return False

    def generate_validator(self, length: int):
        # Generate a completely random string of a given length
        rand_char = 0
        step = 0
        random_code = ''
        while step < length:
            # Start is inclusive, stop is not
            selector = random.randrange(1, 4)
            if selector == 1:
                # 48 - 57: Numbers
                rand_char = random.randrange(48, 58)
            elif selector == 2:
                # 65 - 90: Capitals
                rand_char = random.randrange(65, 91)
            elif selector == 3:
                # 97 - 122: Lower case
                rand_char = random.randrange(97, 123)
            random_code += str(chr(rand_char))
            step += 1
        return random_code


def reset_db():
    db.drop_all(bind=None)
    db.create_all(bind=None)
    db.session.commit()


def create_sample_data():
    aircraft1 = Aircraft(model='Cirrus F4000', registration='NZ1410', capacity=6,
                         retired=False, maintenance_due=datetime(2022, 7, 14))
    aircraft2 = Aircraft(model='Cirrus F4600', registration='NZ1476', capacity=7,
                         retired=False, maintenance_due=datetime(2022, 8, 30))
    airport1 = Airport(icao='NZDF', name='Dairy Flat Airfield')
    airport2 = Airport(icao='NZAA', name='Auckland International Airport')
    airport3 = Airport(icao='NZRT', name='Rotorua Domestic Airport')
    db.session.add(aircraft1)
    db.session.add(aircraft2)
    db.session.add(airport1)
    db.session.add(airport2)
    db.session.add(airport3)
    db.session.commit()
