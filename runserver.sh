#! /bin/bash

# runserver.sh base  --> will execute python manage.py runserver --settings=noteapp.settings.base

setting_module=$1
[[ -z $setting_module ]] && export setting_module=base

python manage.py runserver --settings=noteapp.settings.$setting_module