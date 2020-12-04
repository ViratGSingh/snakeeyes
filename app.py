from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from blueprints.page import page
from blueprints.user import user
from blueprints.user.models import User

from extensions import (
    
    mail,
    db,
    csrf,
    login_manager
)

app = Flask(__name__)
def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.secret_key="a2df83f29994c53909bd65bc0f55c502f57ca305735ab1fe"
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_DEFAULT_SENDER'] = "justlistenmusic99@gmail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "justlistenmusic99@gmail.com"
    app.config['MAIL_PASSWORD'] = "vgs41999"
    
    if settings_override:
        app.config.update(settings_override)
    extensions(app)
    app.register_blueprint(page)
    app.register_blueprint(user)
    
    
    authentication(app, User)
    
    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    
    login_manager.init_app(app)

    return None
def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)
app=create_app()

if __name__ == "main":
    app.run()

