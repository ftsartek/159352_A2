import datetime
import time

import flask_login
from dateutil.tz import tzlocal
from flask import render_template, request, escape, abort, session, redirect, flash
from flask_login import login_required, logout_user, login_user, current_user, login_fresh
from app import app, database, database_defaults, forms, accounts, database_helpers
from datetime import date

print("Initialising routes")

@app.route('/')
def index():
    return render_template("index.jinja")


@app.route('/routes')
def routes():
    return render_template("routes.jinja")


@app.route('/aircraft')
def aircraft():
    return render_template("aircraft.jinja")


# Account transaction pages
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if current_user.is_authenticated:
        return redirect('/dashboard')
    if form.validate_on_submit():
        user = database.User(email=form.email.data, first_name=form.first_name.data, last_name=form.surname.data, active=True)
        user.save_pass_hash(form.password.data)
        user.generate_validator(16)
        database.db.session.add(user)
        database.db.session.commit()
        flash('Your account has been created, and you can now log in.', 'success')
        return redirect('/login')
    elif len(form.errors) > 0:
        issues = ''
        for error in form.errors:
            issues += form.errors.get(error)[0] + '<br>'
        flash(f'Your account could not be created. Errors encountered:<br>' + issues, 'danger')
    return render_template("register.jinja", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if current_user.is_authenticated or login_fresh is None:
        return redirect('/dashboard')
    if form.validate_on_submit():
        user = database.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if not user.validate_pass(form.password.data):
                flash('Incorrect email or password', 'danger')
                return render_template('login.jinja', form=form)
            else:
                login_user(user, remember=True)
                flash('Logged in successfully', 'success')
            return redirect('/dashboard/bookings')
        else:
            flash('Incorrect email or password', 'danger')
    return render_template('login.jinja', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect('/login')


@app.route('/dashboard/validate', methods=['GET', 'POST'])
@login_required
def acc_validate():
    form = forms.ValidationCheckForm()
    if not current_user.requires_validation():
        return redirect('/dashboard')
    if form.validate_on_submit():
        if current_user.validate_account(form.validation_code.data):
            flash('Your account was successfully validated.', 'success')
            database.db.session.commit()
            return redirect('/dashboard')
        else:
            flash('Your account could not be verified. Please try again.', 'danger')
    elif len(form.errors) > 0:
        flash('Your account could not be verified. Please try again.', 'danger')
    return render_template("dashboard_validate.jinja", form=form)


@app.route('/dashboard/booking/confirm/<book_id>')
@login_required
def confirmation(book_id):
    conf_bookings = []
    ref = 'PT' + str(datetime.date.today().year)[2:] + str(current_user.id)
    lookup = database.Booking.query.filter_by(id=book_id).first()
    # Redirect if the ID is invalid
    if lookup is None:
        flash('No booking with this reference exists.', 'danger')
        return redirect('/dashboard/bookings')
    # Check that the user should be allowed to see this confirmation
    if (lookup.user_id == current_user.id and not lookup.cancelled) or current_user.is_admin():
        conf_bookings.append(database_helpers.booking_list(booking=lookup.id)[0])
        # Insert at the start of the list if it's the origin
        if lookup.origin_booking is not None:
            conf_bookings.insert(0, database_helpers.booking_list(booking=lookup.origin_booking)[0])
        # Or append to the end if it's return
        elif lookup.return_booking is not None:
            conf_bookings.append(database_helpers.booking_list(booking=lookup.return_booking)[0])
        # Build a reference number based on IDs
        refno = 0
        total_price = 0
        # Get total price and a reference number
        for item in conf_bookings:
            refno += int((datetime.date.today().month * datetime.date.today().day * item.get("Booking ID")) /
                         (item.get("Creation")).second * (item.get("Creation")).minute)
            total_price += float(item.get("Price"))
        ref = ref + str(refno)
        # Add 'R' to the reference if it's a return flight.
        if len(conf_bookings) > 1:
            ref = ref + 'R'
        return render_template("book_confirm.jinja", total_price=f'{total_price:.2f}', bookings=conf_bookings, ref=ref, title="Booking " + ref)
    # Redirect if the user does not have access to this booking
    else:
        flash('You do not have permission to access this resource.', 'warning')
        return redirect('/dashboard/bookings')


@app.route('/dashboard/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    if not current_user.is_validated():
        return redirect('/dashboard/validate')
    else:
        form = forms.BookingCancelForm()
        if form.validate_on_submit():
            booking = database.Booking.query.filter_by(id=form.booking_id.data).first()
            booking.cancelled = True
            booking.seats = 0
            print(form.related_id.data)
            if form.related_id.data != '':
                related = database.Booking.query.filter_by(id=form.related_id.data).first()
                related.cancelled = True
                related.seats = 0
            database.db.session.commit()
            flash('Your booking has been cancelled. Please contact us if this was done in error.', 'success')
        return render_template('book_list.jinja',
                               booking_data=database_helpers.booking_list(current_user.id),
                               cancel_form=form)


@app.route('/dashboard/book', methods=['GET', 'POST'])
@login_required
def book():
    if not current_user.is_validated():
        return redirect('/dashboard/validate')
    else:
        selectform = forms.BookingSelectForm()
        searchform = forms.BookingSearchForm()
        # Book section
        if selectform.submit.data:
            if selectform.validate_on_submit():
                # Create a new booking
                new_booking = database.Booking(seats=selectform.ticket_number.data,
                                               user_id=selectform.user_id.data,
                                               flight_booked_id=selectform.schedule_id.data,
                                               start_leg_id=selectform.startleg_id.data,
                                               end_leg_id=selectform.endleg_id.data,
                                               origin_booking=selectform.original_id.data)
                database.db.session.add(new_booking)
                # If this is a return flight, update the origin flight
                if selectform.original_id.data is not None:
                    update_booking = database.Booking.query.filter_by(id=selectform.original_id.data).first()
                    update_booking.return_booking = new_booking.id
                database.db.session.commit()
                if selectform.return_ticket.data:
                    # Get airport data for query
                    airport_data = [database.Airport.query.filter_by(id=database.FlightLeg.query.filter_by(id=selectform.endleg_id.data).first().arrival_airport_id).first(),
                                    database.Airport.query.filter_by(id=database.FlightLeg.query.filter_by(id=selectform.startleg_id.data).first().departure_airport_id).first()]
                    # Generate and execute query via helper to get flight list
                    return_date_range = database.FlightSchedule.query.filter_by(id=selectform.schedule_id.data).first().date
                    results = database_helpers.filtered_flight_list(
                        airport_data[0].id, airport_data[1].id,
                        return_date_range + datetime.timedelta(days=1),
                        return_date_range + datetime.timedelta(days=15))

                    # If there are no results, alert user and reload search section
                    return render_template('book_select.jinja', searchform=searchform, selectform=selectform,
                                           airport_data=airport_data, results=results, returning=True, original_flight=new_booking.id)
            else:
                print(selectform.errors)
        # Search section
        if searchform.submit.data:
            if searchform.validate_on_submit():
                # Validate data that we can't via WTForms
                invalidate = False
                if searchform.date_end_selector.data < searchform.date_start_selector.data:
                    flash("Date selection invalid: Range end date is earlier than range start date.", 'warning')
                    invalidate = True
                if searchform.date_start_selector.data < datetime.date.today():
                    flash("Date selection invalid: Cannot search for historic flights.", 'warning')
                    invalidate = True
                if searchform.start_airport.data == '0' or searchform.end_airport.data == '0':
                    flash("Airport selection invalid: Both a departure and arrival airport must be selected.", 'warning')
                    invalidate = True
                elif searchform.start_airport.data == searchform.end_airport.data:
                    flash("Airport selection invalid: Start and end destinations must be different.", 'warning')
                    invalidate = True
                # Reload the first step if the form data is invalid
                if invalidate:
                    return render_template('book_search.jinja', searchform=searchform)
                # Get airport data for query
                airport_data = [database.Airport.query.filter_by(id=searchform.start_airport.data).first(),
                                database.Airport.query.filter_by(id=searchform.end_airport.data).first()]
                # Generate and execute query via helper to get flight list
                results = database_helpers.filtered_flight_list(
                    searchform.start_airport.data, searchform.end_airport.data,
                    searchform.date_start_selector.data, searchform.date_end_selector.data)
                # If there are no results, alert user and reload search section
                if len(results) == 0:
                    flash("No flights fit these criteria. Please try again.", 'warning')
                    return render_template('book_search.jinja', searchform=searchform)
                # If everything is good, move on to booking

                flash(f'{len(results)} flights found matching your criteria.', 'success')
                return render_template('book_select.jinja', searchform=searchform, selectform=selectform, airport_data=airport_data, results=results, returning=False)
        # Default loader
        return render_template('book_search.jinja', searchform=searchform)


@app.route('/admin/bookings')
@login_required
def adm_bookings():
    if current_user.is_admin():
        return render_template("adm_bookings.jinja", booking_data=database_helpers.booking_list())
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/admin/fleet', methods=['GET', 'POST'])
@login_required
def adm_fleet():
    if current_user.is_admin():
        return render_template("adm_fleet.jinja", fleet_data=database.Aircraft.query.all())
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/admin/fleet/edit/<ac_id>', methods=['GET', 'POST'])
@login_required
def adm_fleet_mgmt(ac_id):
    if current_user.is_admin():
        aircraft = database.Aircraft.query.get(ac_id)
        if aircraft is not None:
            form = forms.AircraftEditForm()
            return render_template('adm_fleet_edit.jinja', aircraft=aircraft, form=form)
        # Fallback
        return redirect('/admin/fleet')
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def adm_users():
    if current_user.is_admin():
        return render_template("adm_users.jinja", user_data=database.User.query.all())
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/reset_all')
@login_required
def reset_all():
    if current_user.is_admin():
        if not isinstance(current_user, flask_login.AnonymousUserMixin):
            logout_user()
        database_defaults.generate_defaults()
    else:
        flash("You do not have permission to perform this function", "warning")
    return redirect('/login')
