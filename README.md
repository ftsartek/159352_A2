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

A user can create bookings from search results, look up their bookings (including history), and delete bookings.

#### Additional Features
 - Return Flights: users can optionally book a return flight after making an initial flight selection, with the parameters of the return being automatically chosen (within 2 weeks of the initial flight, return only, no detours). Upon cancelling a flight, any related flights will also be cancelled.