#!/usr/bin/env bash

# Initial system setup. Meant to be run as privileged user.
sudo apt-get update
sudo apt-get upgrade

# System packages
sudo apt-get install -y build-essential
sudo apt-get install -y libssl-dev libffi-dev libmagickwand-dev
sudo apt-get install -y git gettext

sudo apt-get install -y postgresql libpq-dev 
sudo apt-get install -y postgresql-contrib

# Node.js
sudo apt-get install -y python-software-properties python g++ make libmagickwand-dev
sudo apt-get install -y build-essential libssl-dev libffi-dev 
sudo apt-get install -y python-pip python-virtualenv 
sudo apt-get install -y python-dev git gettext

# Setting up PostgreSQL database
sudo -u postgres createdb ajabcapital -T template0 -E UTF8 --locale=en_US.UTF8
echo "CREATE USER ajabcapital WITH PASSWORD 'o94u3n3jJJKS21032sjdu34nsnlp223';" | sudo -u postgres psql
echo "ALTER USER ajabcapital CREATEDB;" | sudo -u postgres psql