from flask import Flask,render_template,request,redirect


from blueprints.page import page



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
    
    app.register_blueprint(page)
    
    
    

    error_templates(app)
    return app



def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)

    return None

app=create_app()

# with app.app_context():
#     db.create_all()
if __name__ == "main":
    app.run()

