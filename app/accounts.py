import sqlalchemy.exc
from flask import flash, redirect
from flask_login import LoginManager
from app import app, database

login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return database.User.query.filter_by(id=int(user_id)).first()
    except sqlalchemy.exc.OperationalError:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('This resource or page requires you to be logged in.', 'danger')
    return redirect('/login')
