import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "secret"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    MAIL_SERVER = '0.0.0.0'
    MAIL_PORT = 1025
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'test@test.com'
    MAIL_MAX_EMAILS = None
    MAIL_DEBUG = False
    FAIL_MAIL_SILENTLY = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_CONNECTION_RETRY_ON_STARTUP = True
    


    

