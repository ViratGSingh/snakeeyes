import os
# SQLAlchemy.
#DATABASE_URL= 'postgresql://postgres:vgs41999@localhost:5432/users'
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_USERNAME='justlistenmusic99@gmail.com'
#DEBUG = True
SECRET_KEY="a2df83f29994c53909bd65bc0f55c502f57ca305735ab1fe"