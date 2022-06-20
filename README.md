## Flight Booking Web App
### 159.352 Assignment 2
#### Jordan Russell - 19039673

FlightBooker is an online booking application built for the fictional airline Premiere Air Travel, who are based out of Dairy Flat Airfield. They offer 6 services, the details of which can be found at '/routes', and utilise 5 aircraft, the details of which are at '/aircraft'. All routes accessible by a given user are accessible via the menu bar.

Upon first starting, the server will generate a set of defaults for databases, including schedules. While these should be useable for the life of the Docker container - however, if something breaks, or you would like to commit a full reset, use the Admin account and navigate to '/reset_all' - this will clear the database and generate a new set of defaults. If the admin account is inaccessible... Well, you'd better spin up a new Docker container, or find a way to delete the sqlite DB.

A test user account is accessible using:
 - testuser@flightbooker.nz
 - n0rmalPass

On its first login, it will require that you verify the account - simply do this by copy-pasting the verification code shown on the page and submitting.

If you'd like to see admin features (full user listing, etc), you can log in with:
 - adminuser@flightbooker.nz
 - 4dminPass

This account will not need verification, and can see a full list of bookings  (by any user) as well as the details of aircraft & users.

It is additionally possible to create a new user account at the '/register' endpoint; as with the standard user, it will require 'verification' upon creation and will always redirect to that page until verification is complete.

A user can create bookings from search results, look up their bookings (including history), and delete bookings.

#### Built With (and why):
 - Back End:
   - Flask: Lightweight, powerful and extensible. I chose Flask because a) I've got some experience with it, and b) it eliminates some of the bloat I feel like Django packages in.
   - SQLAlchemy: An excellent ORM layer for SQL databases. I can pythonise the SQL queries and it simplifies the transactions I need to do with very little overhead. Linked to:
     - SQLite3: While it would be very easy to integrate this with another SQL-style server (PGSql, MySQL), SQLite3 is more than suitable for the job and avoids a lot of the complexity of configuring another DB in a docker container
   - Flask-Login: Easy-to-implement user session management.
   - WTForms: A Python HTML form library, used to 
 - Front End:
   - Javascript: Could've used JQuery or another front-end JS framework, but the implementations in this web app have been fairly straightforward, so there was no real call to do so.
   - Jinja Templating: Dynamic HTML templates with python-esque functionality capabilities. Generated on request and built up into a complete HTML page.
   - Bootstrap: Topped off with some custom CSS, Bootstrap forms the majority of this app's visual implementation. It makes it quick and easy to get a decent-looking basis for a page.

#### Additional Features:
 - Return Flights: users can optionally book a return flight after making an initial flight selection, with the parameters of the return being automatically chosen (within 2 weeks of the initial flight, return only, no detours). Upon cancelling a flight, any related flights will also be cancelled.