from fabric.api import local


def setup_test_env():
    local("./noteapp/envs/test/setup.sh")


def test(app):
    setup_test_env()
    local("./manage.py test {} --settings=noteapp.settings.test".format(app))


def test_notes():
    test(app="notes")


def freeze(requirements="requirements.txt"):
    local("pip freeze > {}".format(requirements))


def run_server(settings="dev"):
    settings_type = "noteapp.settings.{}".format(settings)
    local("./manage.py runserver --settings={}".format(settings_type))