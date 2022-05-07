from datetime import datetime, date, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app
from passlib.hash import sha512_crypt
import random

print("Initialising database")
db = SQLAlchemy(app)


class Aircraft(db.Model):
    __tablename__ = 'aircraft'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(30), nullable=False)
    registration = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    retired = db.Column(db.Boolean, nullable=False, default=False)
    maintenance_due = db.Column(db.Date, nullable=False, default=(date.today() + timedelta(weeks=26)))
    flights = db.relationship('Flight', backref='aircraft', lazy=True, uselist=True)


class Booking(db.Model):
    __tablename__ = 'booking'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tickets = db.relationship('Ticket', backref='booking', lazy=True, uselist=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_booked_id = db.Column(db.Integer, db.ForeignKey('flightschedule.id'), nullable=False)
    start_leg_id = db.Column(db.Integer, db.ForeignKey('flightleg.id'))
    end_leg_id = db.Column(db.Integer, db.ForeignKey('flightleg.id'))
    flight_booked = db.relationship('FlightSchedule', back_populates='bookings', uselist=False)


class FlightSchedule(db.Model):
    __tablename__ = 'flightschedule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    bookings = db.relationship('Booking', back_populates='flight_booked', lazy=True, uselist=True)
    flight = db.relationship('Flight', back_populates='schedule', lazy=True, uselist=False)


class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    designation = db.Column(db.String(8), nullable=False)
    return_flight_id = db.Column(db.String, db.ForeignKey('flight.id'), nullable=True)
    aircraft_id = db.Column(db.String, db.ForeignKey('aircraft.id'), nullable=False)
    flight = db.relationship('FlightLeg', backref='flight', lazy=True, uselist=True)
    schedule = db.relationship('FlightSchedule', back_populates='flight', lazy=True, uselist=True)


# Used to define legs of flights
class FlightLeg(db.Model):
    __tablename__ = 'flightleg'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    leg = db.Column(db.Integer, default=None, nullable=True)
    departure_time = db.Column(db.Time, nullable=False)
    flight_duration = db.Column(db.Time, nullable=False)
    price = db.Column(db.Float, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    # These two don't need to exclude each other to allow for scenic routes that return to the same airport
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    booking_start_leg = db.relationship('Booking', backref='start_leg', lazy=True, uselist=True,
                                        foreign_keys=[Booking.start_leg_id])
    booking_end_leg = db.relationship('Booking', backref='end_leg', lazy=True, uselist=True,
                                      foreign_keys=[Booking.end_leg_id])


class Airport(db.Model):
    __tablename__ = 'airport'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    icao = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    tz_offset = db.Column(db.Interval, nullable=False)
    departures = db.relationship('FlightLeg', backref='departure_airport', lazy=True, uselist=True,
                                 foreign_keys=[FlightLeg.departure_airport_id])
    arrivals = db.relationship('FlightLeg', backref='arrival_airport', lazy=True, uselist=True,
                               foreign_keys=[FlightLeg.arrival_airport_id])


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email: str = db.Column(db.String(30), unique=True, nullable=False)
    first_name: str = db.Column(db.String(20), nullable=False)
    last_name: str = db.Column(db.String(20), nullable=False)
    pass_hash: str = db.Column(db.String(200), nullable=False)
    verification_code: str = db.Column(db.String(20), nullable=True)
    validated: bool = db.Column(db.Boolean, nullable=False, default=False)
    active: bool = db.Column(db.Boolean, nullable=False, default=False)
    admin: bool = db.Column(db.Boolean, nullable=False, default=False)
    bookings = db.relationship('Booking', backref='user', lazy=True, uselist=True)

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.active

    def is_admin(self):
        return self.admin

    def is_validated(self):
        return self.validated

    def get_id(self) -> str:
        return str(self.id)

    def save_pass_hash(self, password) -> None:
        self.pass_hash = sha512_crypt.hash(password)

    def validate_pass(self, password) -> bool:
        return sha512_crypt.verify(password, self.pass_hash)

    def validate_account(self, code) -> bool:
        if self.verification_code == code:
            self.verification_code = None
            self.validated = True
            return True
        else:
            return False

    def requires_validation(self):
        if not self.validated or self.verification_code is not None:
            return True
        else:
            return False

    def generate_validator(self, length: int) -> None:
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
        self.verification_code = random_code