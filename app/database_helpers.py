import datetime

from app.database import db, Flight, FlightSchedule, FlightLeg, Airport, Aircraft, Booking
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
    # One HELL of an SQL query to get all the data we need to check available bookings
    combine = db.select(FlightSchedule.id, FlightSchedule.date, Flight.id,
                        fl1_aliased.id, fl1_aliased.departure_airport_id, fl1_aliased.leg,
                        fl1_aliased.departure_time, fl1_aliased.flight_duration,
                        fl2_aliased.id, fl2_aliased.arrival_airport_id, fl2_aliased.leg,
                        fl2_aliased.departure_time, fl2_aliased.flight_duration,
                        db.func.sum(Booking.seats), Aircraft.id) \
        .where(FlightSchedule.date >= earliest, FlightSchedule.date <= latest) \
        .join(FlightSchedule.flight.of_type(Flight)).outerjoin(Booking) \
        .join(Flight.aircraft.of_type(Aircraft)) \
        .join(Flight.flightlegs.of_type(fl1_aliased)).join(Flight.flightlegs.of_type(fl2_aliased)) \
        .where(fl1_aliased.departure_airport_id == departure) \
        .where(fl2_aliased.arrival_airport_id == arrival) \
        .group_by(FlightSchedule.id)
    # Execute the command
    schedules = db.session.execute(combine)
    dict_list = []
    # Loop through results and build a dictionary to return (easier to work with)
    for item in schedules:
        dict_list.append({
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
        })
    return dict_list
