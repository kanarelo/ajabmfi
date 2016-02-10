#!/usr/bin/env bash

# Sets up Django project. Meant to be run as non-privileged user (vagrant).

# Setting up virtualenv and istalling Python packages

virtualenv --python=python2.7 ~/venv
source ~/venv/bin/activate
cd /ajabcapital/
pip install -r requirements/dev.pip

# Creating tables and populating the database
python manage.py migrate
