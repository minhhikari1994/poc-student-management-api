#!/bin/sh
flask db upgrade
gunicorn -b 0.0.0.0:5000 -w 4 "poc-api:create_app()"