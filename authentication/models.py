from django_mongoengine.mongo_auth.models import User


class Account(User):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
