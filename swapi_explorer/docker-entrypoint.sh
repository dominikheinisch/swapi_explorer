#!/usr/bin/env bash

./wait-for-it.sh postgres:5432 &&
python manage.py makemigrations &&
python manage.py migrate