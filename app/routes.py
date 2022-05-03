import flask
from flask import render_template, request, escape, abort, session, redirect, flash
from flask_login import login_required, logout_user, login_user
from app import app, database, forms, accounts
from passlib.hash import sha512_crypt


@app.route('/')
def index():
    return render_template("index.jinja")


@app.route('/routes')
def routes():
    return render_template("routes.jinja")


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    print(flask.get_flashed_messages(with_categories=True))
    if form.validate_on_submit():
        user = database.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if not user.validate_pass(form.password.data):
                flash('Incorrect username or password', 'danger')
                return render_template('login.jinja', form=form)
            else:
                login_user(user)
                flash('Logged in successfully', 'success')
            return redirect('/')
        else:
            flash('Incorrect username or password', 'danger')
    return render_template('login.jinja', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/account')
@login_required
def account():
    pass


@app.route('/account/pwd_reset', methods=['GET', 'POST'])
@login_required
def pwd_reset():
    pass


@app.route('/account/acc_validate', methods=['GET', 'POST'])
@login_required
def acc_validate():
    pass


@app.route('/account/bookings')
@login_required
def bookings():
    pass


@app.route('/account/book')
@login_required
def book():
    pass


@app.route('/admin/bookings')
@login_required
def adm_bookings():
    pass


@app.route('/admin/schedule', methods=['GET', 'POST'])
@login_required
def adm_schedule():
    pass


@app.route('/admin/fleet', methods=['GET', 'POST'])
@login_required
def adm_fleet():
    return render_template("adm_fleet.jinja", fleet_data=database.Aircraft.query.all())


@app.route('/admin/fleet/manage', methods=['GET', 'POST'])
@login_required
def adm_fleet_mgmt():
    if request.method == 'POST':
        post_data = request.values.to_dict()
        if post_data.get("aircraft_id") is not None:
            aircraft = database.Aircraft.query.filter_by(id=post_data.get("aircraft_id")).first()
            if post_data.get("return_mode") == "Save":
                # Save post data to aircraft
                pass
            elif post_data.get("return_mode") == "New":
                # Save post data to a new aircraft
                pass
            return render_template('adm_fleet_mgmt.jinja', aircraft=aircraft)
    # Fallback
    return redirect('/admin/fleet')


@app.route('/admin/routes', methods=['GET', 'POST'])
@login_required
def adm_routes():
    pass


@app.route('/admin/accounts', methods=['GET', 'POST'])
@login_required
def adm_accounts():
    pass


