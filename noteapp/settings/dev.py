import mongoengine
from .base import *

DEBUG = True

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.dummy'}
}


SESSION_ENGINE = 'mongoengine.django.sessions'

MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_HOST = os.environ.get("MONGODB_HOST")
MONGODB_PORT = os.environ.get("MONGODB_PORT")
MONGODB_NAME = os.environ.get("MONGODB_NAME")

MONGODB_DATABASE = (
    'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@'
    '{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_NAME}'.format(**locals()))

MONGO_DATABASE_OPTIONS = {
    "host": MONGODB_HOST,
    "port": int(MONGODB_PORT),
    "username": MONGODB_USER,
    "password": MONGODB_PASSWORD,
}


#mongoengine.connect(MONGODB_NAME, host=MONGODB_DATABASE)
mongoengine.register_connection(
    'default', MONGODB_NAME, **MONGO_DATABASE_OPTIONS)


AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)