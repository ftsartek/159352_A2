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
    combine = db.select(FlightSchedule.id, FlightSchedule.date, Flight.id, fl1_aliased.id,
                        fl1_aliased.departure_airport_id, fl2_aliased.id, fl2_aliased.arrival_airport_id,
                        db.func.count(Booking.flight_booked_id), Aircraft.capacity) \
        .where(FlightSchedule.date >= earliest, FlightSchedule.date <= latest) \
        .join(FlightSchedule.flight.of_type(Flight)).outerjoin(Booking) \
        .join(Flight.aircraft.of_type(Aircraft)) \
        .join(Flight.flightlegs.of_type(fl1_aliased)).join(Flight.flightlegs.of_type(fl2_aliased)) \
        .where(fl1_aliased.departure_airport_id == departure) \
        .where(fl2_aliased.arrival_airport_id == arrival) \
        .group_by(FlightSchedule.id)


    schedules = db.session.execute(combine)
    schedule_list = [item for item in schedules]
    print(schedule_list)
    #return schedules
