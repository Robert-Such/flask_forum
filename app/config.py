"""App configuration."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SLF_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('EMAIL_USER')
    MAIL_PASSWORD = environ.get('EMAIL_PASS')
    FLASK_ENV = environ.get('FLASK_ENV')
