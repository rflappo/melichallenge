#!/usr/bin/env bash

export FLASK_APP='app.__init__.py'
export APP_SETTINGS='app.config.DevelopmentConfig'
export DATABASE_URL='postgres://melichallenge:melichallenge@127.0.0.1:54320/melichallenge'

python manage.py shell
