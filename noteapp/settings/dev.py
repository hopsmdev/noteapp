import mongoengine
from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': '',
    },
}

SESSION_ENGINE = 'mongoengine.django.sessions'

MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASSWD = os.environ.get("MONGODB_PASSWD")
MONGODB_HOST = os.environ.get("MONGODB_HOST")
MONGODB_NAME = os.environ.get("MONGODB_NAME")

mongoengine.connect(MONGODB_NAME,
                    host=('mongodb://{MONGODB_USER}:{MONGODB_PASSWD}@'
                          '{MONGODB_HOST}/{MONGODB_NAME}'.format(**locals())))

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)