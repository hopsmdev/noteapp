from fabric.api import local


def setup_test_env():
    local("./noteapp/envs/test/setup.sh")


def test(app):
    setup_test_env()
    local("./manage.py test {} -p tests_*.py "
          "--settings=noteapp.settings.test".format(app))


def test_model(app):
    setup_test_env()
    local("./manage.py test {} "
          "-p tests_model.py --settings=noteapp.settings.test".format(app))


def test_api(app):
    setup_test_env()
    local("./manage.py test {} "
          "-p tests_api.py --settings=noteapp.settings.test".format(app))


def freeze(requirements="requirements.txt"):
    local("pip freeze > {}".format(requirements))


def run_server(settings="dev"):

    local("python load_data.py")

    settings_type = "noteapp.settings.{}".format(settings)
    local("./manage.py runserver --settings={} --verbosity 3".format(
        settings_type))