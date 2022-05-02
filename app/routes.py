from flask import render_template, request, escape, abort, session, redirect
from app import app, database, forms
from passlib.hash import sha512_crypt

@app.route('/')
def index():
    return render_template("index.jinja")


@app.route('/routes')
def routes():
    return render_template("routes.jinja")


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass


@app.route('/account/pwd_reset', methods=['GET', 'POST'])
def pwd_reset():
    pass


@app.route('/account/acc_validate', methods=['GET', 'POST'])
def acc_validate():
    pass


@app.route('/account/bookings')
def bookings():
    pass


@app.route('/account/book')
def book():
    pass


@app.route('/admin/bookings')
def adm_bookings():
    pass


@app.route('/admin/schedule', methods=['GET', 'POST'])
def adm_schedule():
    pass


@app.route('/admin/fleet', methods=['GET', 'POST'])
def adm_fleet():
    return render_template("adm_fleet.jinja", fleet_data=database.Aircraft.query.all())


@app.route('/admin/fleet/manage', methods=['GET', 'POST'])
def adm_fleet_mgmt():
    if request.method == 'POST':
        post_data = request.values.to_dict()
        if post_data.get("aircraft_id") is not None:
            aircraft = database.Aircraft.query.filter_by(id=post_data.get("aircraft_id")).first()
            if post_data.get("return_mode") == "Save":
                # Save post data to aircraft
                pass
            print(aircraft.maintenance_due)
            return render_template('adm_fleet_mgmt.jinja', aircraft=aircraft)
    # Fallback
    return redirect('/admin/fleet')


@app.route('/admin/routes', methods=['GET', 'POST'])
def adm_routes():
    pass


@app.route('/admin/accounts', methods=['GET', 'POST'])
def adm_accounts():
    pass


