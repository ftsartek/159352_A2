from flask_login import LoginManager
from app import app, database

login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return database.User.query.filter_by(id=user_id).first()
