from app.database import db, Flight, FlightSchedule, FlightLeg, Airport
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
    query = db.select(Flight).outerjoin(Flight.schedule).\
        where(FlightSchedule.date <= latest, FlightSchedule.date >= earliest)
    print(query)
    schedules = db.session.execute(query)
    for item in schedules:
        print(item.Flight.designation, item.Flight.schedule.date)
    return schedules
