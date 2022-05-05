from flask import render_template, request, escape, abort, session, redirect, flash
from flask_login import login_required, logout_user, login_user, current_user, login_fresh
from app import app, database, forms, accounts


@app.route('/')
def index():
    return render_template("index.jinja")


@app.route('/routes')
def routes():
    return render_template("routes.jinja")


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
                flash('Incorrect username or password', 'danger')
                return render_template('login.jinja', form=form)
            else:
                login_user(user, remember=True)
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


@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_validated():
        return redirect('/dashboard/validate')
    return "Hi"


@app.route('/dashboard/pwd_reset', methods=['GET', 'POST'])
@login_required
def pwd_reset():
    if not current_user.is_validated():
        return redirect('/dashboard/validate')
    pass


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


@app.route('/dashboard/bookings')
@login_required
def bookings():
    if not current_user.is_validated():
        return redirect('/dashboard/validate')
    pass


@app.route('/dashboard/book')
@login_required
def book():
    if not current_user.is_validated():
        return redirect('/dashboard/validate')
    pass


@app.route('/admin/dashboard')
@login_required
def adm_dash():
    if current_user.is_admin():
        return render_template("adm_.jinja")
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/admin/bookings')
@login_required
def adm_bookings():
    if current_user.is_admin():
        return render_template("adm_.jinja")
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/admin/schedule', methods=['GET', 'POST'])
@login_required
def adm_schedule():
    if current_user.is_admin():
        return render_template("adm_.jinja")
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
        if request.method == 'GET':
            aircraft = database.Aircraft.query.filter_by(id=ac_id).first()
            if aircraft is not None:
                form = forms.AircraftEditForm()
                return render_template('adm_fleet_edit.jinja', aircraft=aircraft, form=form)
            # Fallback
            return redirect('/admin/fleet')
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/admin/routes', methods=['GET', 'POST'])
@login_required
def adm_routes():
    if current_user.is_admin():
        return render_template("adm_.jinja")
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/admin/accounts', methods=['GET', 'POST'])
@login_required
def adm_accounts():
    if current_user.is_admin():
        return render_template("adm_.jinja")
    else:
        flash("You do not have permission to view this page.", "warning")
        return redirect('/dashboard')


@app.route('/resetall')
def reset_all():
    database.reset_db()
    database.create_sample_data()
    return redirect('/login')
