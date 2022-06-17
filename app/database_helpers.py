import datetime
import time

from app.database import db, Flight, FlightSchedule, FlightLeg, Airport, Aircraft, Booking, User
from datetime import date


def flight_list():
    flights = Flight.query.all()
    choice_list = []
    for flight in flights:
        legs = flight.flightlegs
        start_incrementor = 0
        while start_incrementor < len(legs):
            end_incrementor = start_incrementor
            while end_incrementor < len(legs):
                choice_list.append(
                    ((flight.id, legs[start_incrementor].id, legs[end_incrementor].id),
                     f"{flight.designation}: {legs[start_incrementor].departure_airport.name} --> {legs[end_incrementor].arrival_airport.name}"))
                end_incrementor += 1
            start_incrementor += 1
    return choice_list


def filtered_flight_list(departure: int, arrival: int, earliest: date, latest: date):
    # Alias two versions of FlightLeg for startleg and endleg comparisons
    fl1_aliased = db.aliased(FlightLeg)
    fl2_aliased = db.aliased(FlightLeg)
    # One HELL of an SQL query to get all the data we need to check available bookings.
    # The code is a little messier than a series of queries, but it's more efficient.
    combine = db.select(FlightSchedule.id, FlightSchedule.date, Flight.id,
                        fl1_aliased.id, fl1_aliased.departure_airport_id, fl1_aliased.leg,
                        fl1_aliased.departure_time, fl1_aliased.flight_duration,
                        fl2_aliased.id, fl2_aliased.arrival_airport_id, fl2_aliased.leg,
                        fl2_aliased.departure_time, fl2_aliased.flight_duration,
                        db.func.sum(Booking.seats), Aircraft.id) \
        .where(FlightSchedule.date >= earliest, FlightSchedule.date <= latest) \
        .join(FlightSchedule.flight.of_type(Flight)) \
        .join(Flight.aircraft.of_type(Aircraft)) \
        .join(Flight.flightlegs.of_type(fl1_aliased)).join(Flight.flightlegs.of_type(fl2_aliased)) \
        .outerjoin(FlightSchedule.bookings.and_(
        db.and_(Booking.start_leg_id <= fl2_aliased.id, Booking.end_leg_id >= fl1_aliased.id))) \
        .where(fl1_aliased.departure_airport_id == departure) \
        .where(fl2_aliased.arrival_airport_id == arrival) \
        .group_by(FlightSchedule.id)
    # Execute the command
    schedules = db.session.execute(combine)
    compiled_schedules = []
    # Loop through results and build a dictionary to return (easier to work with)
    for item in schedules:
        compiled_schedules.append({
            "Schedule ID": item[0],
            "Schedule Date": item[1],
            "Flight Designation": Flight.query.filter_by(id=item[2]).first().designation,
            "Flight Image": Flight.query.filter_by(id=item[2]).first().route_image if not None else "route_missing.png",
            "Aircraft Model": Aircraft.query.filter_by(id=item[14]).first().model,
            "Start Leg ID": item[3],
            "Departure Airport Name": Airport.query.filter_by(id=item[4]).first().name,
            "Departure Airport ICAO": Airport.query.filter_by(id=item[4]).first().icao,
            "Stops": item[10] - item[5],
            "Start Leg Departure": datetime.datetime.combine(item[1], item[6]),
            "End Leg ID": item[8],
            "Arrival Airport Name": Airport.query.filter_by(id=item[9]).first().name,
            "Arrival Airport ICAO": Airport.query.filter_by(id=item[9]).first().icao,
            "End Leg Arrival": datetime.datetime.combine(item[1], item[6]) + item[12],
            "Scheduled Seat Bookings": item[13] if item[13] is not None else 0,
            "Aircraft Capacity": Aircraft.query.filter_by(id=item[14]).first().capacity,
            "Price": f"{calc_total_price(item[2], item[3], item[8]):.2f}",
        })
    return compiled_schedules


def booking_list(user=None, booking=None):
    fl1_aliased = db.aliased(FlightLeg)
    fl2_aliased = db.aliased(FlightLeg)
    ap1_aliased = db.aliased(Airport)
    ap2_aliased = db.aliased(Airport)
    filters = []
    if user is not None:
        filters.append(Booking.user_id == user)
        filters.append(Booking.cancelled == False)
    if booking is not None:
        filters.append(Booking.id == booking)
    bookings = db.select(Booking.id, Booking.seats, User.id, User.email, FlightSchedule.date, Flight.designation,
                         Aircraft.model, Aircraft.registration, fl1_aliased.departure_time,
                         fl2_aliased.departure_time, fl2_aliased.flight_duration, ap1_aliased.name,
                         ap1_aliased.tz_offset, ap2_aliased.name, ap2_aliased.tz_offset, Booking.origin_booking,
                         Booking.return_booking, Booking.created, Flight.id, fl1_aliased.id, fl2_aliased.id,
                         Booking.cancelled) \
        .select_from(Booking) \
        .join(User, User.id == Booking.user_id) \
        .join(FlightSchedule, Booking.flight_booked_id == FlightSchedule.id) \
        .join(Flight, FlightSchedule.flight_id == Flight.id) \
        .join(Aircraft, Flight.aircraft_id == Aircraft.id) \
        .join(fl1_aliased, fl1_aliased.id == Booking.start_leg_id) \
        .join(fl2_aliased, fl2_aliased.id == Booking.end_leg_id) \
        .join(ap1_aliased, fl1_aliased.departure_airport_id == ap1_aliased.id) \
        .join(ap2_aliased, fl2_aliased.arrival_airport_id == ap2_aliased.id) \
        .group_by(Booking.id).filter(*filters)

    booked = db.session.execute(bookings)
    compiled_bookings = []
    for entry in booked:
        compiled_bookings.append({
            "Booking ID": entry[0],
            "Booked Seats": entry[1],
            "User ID": entry[2],
            "User Email": entry[3],
            "Flight Designation": entry[5],
            "Aircraft Model": entry[6],
            "Aircraft Registration": entry[7],
            "Departure": datetime.datetime.combine(entry[4], entry[8], tzinfo=datetime.timezone(offset=entry[12])),
            "Arrival": datetime.datetime.combine(entry[4], entry[9], tzinfo=datetime.timezone(offset=entry[14])) +
                       entry[10] - (entry[12] - entry[14]),
            "Departure Airport Name": entry[11],
            "Departure Offset": entry[12],
            "Arrival Airport Name": entry[13],
            "Arrival Offset": entry[14],
            "Origin Booking ID": entry[15],
            "Return Booking ID": entry[16],
            "Price": f"{calc_total_price(entry[18], entry[19], entry[20]):.2f}",
            "Creation": entry[17],
            "Cancelled": entry[21],
            "Completed": True if datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=-time.timezone))) > datetime.datetime.combine(entry[4], entry[9], tzinfo=datetime.timezone(offset=entry[14])) +
                       entry[10] - (entry[12] - entry[14]) else False})
    return compiled_bookings


def calc_total_price(flight, start_leg, end_leg):
    price = 0.0
    for leg in range(start_leg, end_leg + 1):
        fl = FlightLeg.query.filter_by(id=leg).first()
        if fl.flight_id == flight:
            price += fl.price
    return price
