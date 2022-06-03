from app.database import db, Aircraft, Airport, Booking, Flight, FlightLeg, FlightSchedule, User
from datetime import date, time, timezone, timedelta
from passlib.hash import sha512_crypt
from os.path import exists

print("Initialising database defaults")


def create_date_list(days) -> tuple:
    date_generator = date.today()
    counter = 0
    date_list = []
    while counter < days:
        date_list.append(date_generator)
        date_generator = date_generator + timedelta(hours=24)
        counter += 1
    return tuple(date_list)


def default_aircraft() -> None:
    syberjet = Aircraft(model='SyberJet SJ30i', registration='NZ1410', capacity=6)
    cirrus1 = Aircraft(model='Cirrus SF50', registration='NZ1675', capacity=4)
    cirrus2 = Aircraft(model='Cirrus SF50', registration='NZ1882', capacity=4)
    hondajet1 = Aircraft(model='HondaJet Elite S', registration='NZ1905', capacity=5)
    hondajet2 = Aircraft(model='HondaJet Elite S', registration='NZ1121', capacity=5)
    db.session.add(syberjet)
    db.session.add(cirrus1)
    db.session.add(cirrus2)
    db.session.add(hondajet1)
    db.session.add(hondajet2)
    db.session.commit()


def default_airports() -> None:
    dairy_flat = Airport(icao='NZNE', name='North Shore Aerodrome', tz_offset=timedelta(hours=12),
                         location='Dairy Flat, Auckland, North Island, New Zealand')
    sydney = Airport(icao='YSSY', name='Sydney Kingsford Smith Airport', tz_offset=timedelta(hours=10),
                     location='Mascot, Sydney, New South Wales, Australia')
    rotorua = Airport(icao='NZRO', name='Rotorua Airport', tz_offset=timedelta(hours=12),
                      location='Rotokawa, Rotorua, North Island, New Zealand')
    tuuta = Airport(icao='NZCI', name='Tuuta Airport', tz_offset=timedelta(hours=12, minutes=45),
                    location='Waitangi, Chatham Island, Wharekauri, New Zealand')
    claris = Airport(icao='NZGB', name='Great Barrier Aerodrome', tz_offset=timedelta(hours=12),
                     location='Claris, Great Barrier Island, New Zealand')
    tekapo = Airport(icao='NZTL', name='Lake Tekapo Airport', tz_offset=timedelta(hours=12),
                     location='Lake Tekapo, Mackenzie District, South Island, New Zealand')
    db.session.add(dairy_flat)
    db.session.add(sydney)
    db.session.add(rotorua)
    db.session.add(tuuta)
    db.session.add(claris)
    db.session.add(tekapo)
    db.session.commit()


def default_users() -> None:
    admin = User(email="adminuser@flightbooker.nz", first_name="admin", last_name="user",
                 pass_hash=sha512_crypt.hash("4dminPass"), admin=True, active=True, validated=True)
    user = User(email="testuser@flightbooker.nz", first_name="normal", last_name="user",
                pass_hash=sha512_crypt.hash("n0rmalPass"), admin=False, active=True, validated=False)
    user.generate_validator(16)
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()


def default_flights() -> None:
    # North/East flights tend to be even numbers. Multiple repeat flights in a day usually get their own designator
    # International are usually between 100-399, domestic are usually 400-999
    # Prestige round flights
    prestige_west = Flight(designation='AFB153', aircraft_id=Aircraft.query.filter_by(registration='NZ1410').first().id, route_image='nzne-yssy.gif')
    prestige_east = Flight(designation='AFB154', aircraft_id=Aircraft.query.filter_by(registration='NZ1410').first().id, route_image='yssy-nzne.gif')
    prestige_west.return_flight_id = prestige_east.id
    prestige_east.return_flight_id = prestige_west.id
    db.session.add(prestige_west)
    db.session.add(prestige_east)
    # Early Rotorua shuttle
    shuttle_early_south = Flight(designation='AFB635',
                                 aircraft_id=Aircraft.query.filter_by(registration='NZ1675').first().id, route_image='nzne-nzro.gif')
    shuttle_early_north = Flight(designation='AFB636',
                                 aircraft_id=Aircraft.query.filter_by(registration='NZ1675').first().id, route_image='nzro-nzne.gif')
    shuttle_early_south.return_flight_id = shuttle_early_north.id
    shuttle_early_north.return_flight_id = shuttle_early_south.id
    db.session.add(shuttle_early_south)
    db.session.add(shuttle_early_north)
    # Late Rotorua shuttle
    shuttle_late_south = Flight(designation='AFB637', aircraft_id=Aircraft.query.filter_by(registration='NZ1675').first().id, route_image='nzne-nzro.gif')
    shuttle_late_north = Flight(designation='AFB638', aircraft_id=Aircraft.query.filter_by(registration='NZ1675').first().id, route_image='nzro-nzne.gif')
    shuttle_late_south.return_flight_id = shuttle_late_north.id
    shuttle_late_north.return_flight_id = shuttle_late_south.id
    db.session.add(shuttle_late_south)
    db.session.add(shuttle_late_north)
    # GBI service
    gbi_east = Flight(designation='AFB700', aircraft_id=Aircraft.query.filter_by(registration='NZ1882').first().id, route_image='nzne-nzgb.gif')
    gbi_west = Flight(designation='AFB701', aircraft_id=Aircraft.query.filter_by(registration='NZ1882').first().id, route_image='nzgb-nzne.gif')
    gbi_east.return_flight_id = gbi_west.id
    gbi_west.return_flight_id = gbi_east.id
    db.session.add(gbi_east)
    db.session.add(gbi_west)
    # Chatham service
    cht_south = Flight(designation='AFB465', aircraft_id=Aircraft.query.filter_by(registration='NZ1905').first().id, route_image='nzne-nzci.gif')
    cht_north = Flight(designation='AFB466', aircraft_id=Aircraft.query.filter_by(registration='NZ1905').first().id, route_image='nzci-nzne.gif')
    cht_south.return_flight_id = cht_north.id
    cht_north.return_flight_id = cht_south.id
    db.session.add(cht_south)
    db.session.add(cht_north)
    # Tekapo Service
    tek_south = Flight(designation='AFB989', aircraft_id=Aircraft.query.filter_by(registration='NZ1121').first().id, route_image='nzne-nztl.gif')
    tek_north = Flight(designation='AFB990', aircraft_id=Aircraft.query.filter_by(registration='NZ1121').first().id, route_image='nztl-nzne.gif')
    tek_south.return_flight_id = tek_north.id
    tek_north.return_flight_id = tek_south.id
    db.session.add(tek_south)
    db.session.add(tek_north)
    # Commit
    db.session.commit()


def default_legs() -> None:
    # Purely because one flight has two legs... Fun!
    # Times are all in UTC only!
    # Prestige Flight Legs
    prst_west_leg1 = FlightLeg(leg=1, price=148.50, flight_duration=timedelta(hours=0, minutes=45),
                               departure_time=time(hour=7, minute=15,
                                                   tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                               flight_id=Flight.query.filter_by(designation='AFB153').first().id,
                               departure_airport_id=Airport.query.filter_by(icao='NZNE').first().id,
                               arrival_airport_id=Airport.query.filter_by(icao='NZRO').first().id)
    prst_west_leg2 = FlightLeg(leg=2, price=551.30, flight_duration=timedelta(hours=4, minutes=15),
                               departure_time=time(hour=8, minute=25,
                                                   tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                               flight_id=Flight.query.filter_by(designation='AFB153').first().id,
                               departure_airport_id=Airport.query.filter_by(icao='NZRO').first().id,
                               arrival_airport_id=Airport.query.filter_by(icao='YSSY').first().id)
    prst_east_leg = FlightLeg(leg=1, price=585.80, flight_duration=timedelta(hours=3, minutes=50),
                              departure_time=time(hour=15, minute=30,
                                                  tzinfo=timezone(offset=timedelta(hours=10), name='AEST')),
                              flight_id=Flight.query.filter_by(designation='AFB154').first().id,
                              departure_airport_id=Airport.query.filter_by(icao='YSSY').first().id,
                              arrival_airport_id=Airport.query.filter_by(icao='NZNE').first().id)
    db.session.add(prst_west_leg1)
    db.session.add(prst_west_leg2)
    db.session.add(prst_east_leg)
    # Early Shuttle Legs
    shtl_south_leg_early = FlightLeg(leg=1, price=98.95, flight_duration=timedelta(hours=0, minutes=55),
                                     departure_time=time(hour=8, minute=0,
                                                         tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                                     flight_id=Flight.query.filter_by(designation='AFB635').first().id,
                                     departure_airport_id=Airport.query.filter_by(icao='NZNE').first().id,
                                     arrival_airport_id=Airport.query.filter_by(icao='NZRO').first().id)
    shtl_north_leg_early = FlightLeg(leg=1, price=99.15, flight_duration=timedelta(hours=0, minutes=58),
                                     departure_time=time(hour=12, minute=0,
                                                         tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                                     flight_id=Flight.query.filter_by(designation='AFB636').first().id,
                                     departure_airport_id=Airport.query.filter_by(icao='NZRO').first().id,
                                     arrival_airport_id=Airport.query.filter_by(icao='NZNE').first().id)
    db.session.add(shtl_south_leg_early)
    db.session.add(shtl_north_leg_early)
    # Late Shuttle Legs
    shtl_south_leg_late = FlightLeg(leg=1, price=98.95, flight_duration=timedelta(hours=0, minutes=55),
                                    departure_time=time(hour=16, minute=0,
                                                        tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                                    flight_id=Flight.query.filter_by(designation='AFB637').first().id,
                                    departure_airport_id=Airport.query.filter_by(icao='NZNE').first().id,
                                    arrival_airport_id=Airport.query.filter_by(icao='NZRO').first().id)
    shtl_north_leg_late = FlightLeg(leg=1, price=99.15, flight_duration=timedelta(hours=0, minutes=58),
                                    departure_time=time(hour=20, minute=0,
                                                        tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                                    flight_id=Flight.query.filter_by(designation='AFB638').first().id,
                                    departure_airport_id=Airport.query.filter_by(icao='NZRO').first().id,
                                    arrival_airport_id=Airport.query.filter_by(icao='NZNE').first().id)
    db.session.add(shtl_south_leg_late)
    db.session.add(shtl_north_leg_late)
    # Great Barrier Island Legs
    gbi_east_leg = FlightLeg(leg=1, price=68.45, flight_duration=timedelta(hours=0, minutes=30),
                             departure_time=time(hour=8, minute=45,
                                                 tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                             flight_id=Flight.query.filter_by(designation='AFB700').first().id,
                             departure_airport_id=Airport.query.filter_by(icao='NZNE').first().id,
                             arrival_airport_id=Airport.query.filter_by(icao='NZGB').first().id)
    gbi_west_leg = FlightLeg(leg=1, price=68.45, flight_duration=timedelta(hours=0, minutes=30),
                             departure_time=time(hour=8, minute=45,
                                                 tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                             flight_id=Flight.query.filter_by(designation='AFB701').first().id,
                             departure_airport_id=Airport.query.filter_by(icao='NZGB').first().id,
                             arrival_airport_id=Airport.query.filter_by(icao='NZNE').first().id)
    db.session.add(gbi_east_leg)
    db.session.add(gbi_west_leg)
    db.session.add(gbi_west_leg)
    # Chatham Island Legs
    chtm_south_leg = FlightLeg(leg=1, price=339.95, flight_duration=timedelta(hours=2, minutes=40),
                               departure_time=time(hour=10, minute=30,
                                                   tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                               flight_id=Flight.query.filter_by(designation='AFB465').first().id,
                               departure_airport_id=Airport.query.filter_by(icao='NZNE').first().id,
                               arrival_airport_id=Airport.query.filter_by(icao='NZCI').first().id)
    chtm_north_leg = FlightLeg(leg=1, price=349.95, flight_duration=timedelta(hours=2, minutes=55),
                               departure_time=time(hour=10, minute=15,
                                                   tzinfo=timezone(offset=timedelta(hours=12, minutes=45), name='NZST')),
                               flight_id=Flight.query.filter_by(designation='AFB466').first().id,
                               departure_airport_id=Airport.query.filter_by(icao='NZCI').first().id,
                               arrival_airport_id=Airport.query.filter_by(icao='NZNE').first().id)
    db.session.add(chtm_south_leg)
    db.session.add(chtm_north_leg)
    # Tekapo Legs
    tek_south_leg = FlightLeg(leg=1, price=385.55, flight_duration=timedelta(hours=3, minutes=15),
                              departure_time=time(hour=10, minute=30,
                                                  tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                              flight_id=Flight.query.filter_by(designation='AFB989').first().id,
                              departure_airport_id=Airport.query.filter_by(icao='NZNE').first().id,
                              arrival_airport_id=Airport.query.filter_by(icao='NZTL').first().id)
    tek_north_leg = FlightLeg(leg=1, price=399.80, flight_duration=timedelta(hours=3, minutes=25),
                              departure_time=time(hour=10, minute=30,
                                                  tzinfo=timezone(offset=timedelta(hours=12), name='NZST')),
                              flight_id=Flight.query.filter_by(designation='AFB990').first().id,
                              departure_airport_id=Airport.query.filter_by(icao='NZTL').first().id,
                              arrival_airport_id=Airport.query.filter_by(icao='NZNE').first().id)
    db.session.add(tek_north_leg)
    db.session.add(tek_south_leg)
    # Commit
    db.session.commit()


def generate_schedule() -> None:
    date_list = create_date_list(365)
    for scheduler_date in date_list:
        weekday = scheduler_date.isoweekday()
        # Shuttle routes
        if weekday in [1, 2, 3, 4, 5]:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB635').first().id))
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB636').first().id))
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB637').first().id))
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB638').first().id))
        # Prestige routes
        if weekday == 5:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB153').first().id))
        if weekday == 7:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB154').first().id))
        # GBI routes
        if weekday in [1, 3, 5]:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB700').first().id))
        if weekday in [2, 4, 6]:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB701').first().id))
        # Chatham routes
        if weekday in [2, 5]:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB465').first().id))
        if weekday in [3, 6]:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB466').first().id))
        # Tekapo routes
        if weekday == 1:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB989').first().id))
        if weekday == 5:
            db.session.add(
                FlightSchedule(date=scheduler_date, flight_id=Flight.query.filter_by(designation='AFB990').first().id))
        db.session.commit()


def generate_defaults() -> None:
    db.drop_all(bind=None)
    db.create_all(bind=None)
    db.session.commit()
    default_aircraft()
    default_airports()
    default_users()
    default_flights()
    default_legs()
    generate_schedule()


if not exists('/tmp/test.db'):
    generate_defaults()
