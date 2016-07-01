import mongoengine
from .base import *

DEBUG = True

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.dummy'}
}

SESSION_ENGINE = 'mongoengine.django.sessions'

MONGODB_NAME = "testdb"

MONGO_DATABASE_OPTIONS = {
    "host": '127.0.0.1',
    "port": 27017,
    "username": 'test',
    "password": 'test',
}

#mongoengine.connect(MONGODB_NAME, host=MONGODB_DATABASE)
mongoengine.register_connection(
    'default', MONGODB_NAME, **MONGO_DATABASE_OPTIONS)


AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)