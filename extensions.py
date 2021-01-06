
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

