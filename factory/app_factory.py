import os
from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from sqlalchemy import inspect

from models.alchemy import db
from models.alchemy import User
from controllers.dataset_controller import dataset_controller_blueprint

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def create_app():
    template_dir = os.path.abspath('./templates')
    app = Flask(__name__, template_folder=template_dir)

    login_manager.init_app(app)

    # Set secret key
    app.config['SECRET_KEY'] = 'thisisasecret'

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)  # Initialize db with app

    # Configure server-side session with SQLAlchemy
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'session'
    Session(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        inspect(db.engine)

    # Register blueprints
    app.register_blueprint(dataset_controller_blueprint)

    return app
