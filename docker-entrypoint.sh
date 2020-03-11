#!/bin/bash

# set the target postgresql host
[ -z $TIMESCALEDB_HOST ] || sed -i "s/DATABASE_HOST=localhost/DATABASE_HOST=$TIMESCALEDB_HOST/g" ./.env
[ -z $TIMESCALEDB_PORT ] || sed -i "s/DATABASE_PORT=5432/DATABASE_PORT=$TIMESCALEDB_PORT/g" ./.env
[ -z $TIMESCALEDB_NAME ] || sed -i "s/DATABASE_NAME=brewmaster/DATABASE_NAME=$TIMESCALEDB_NAME/g" ./.env
[ -z $TIMESCALEDB_USER ] || sed -i "s/DATABASE_USER=postgres/DATABASE_USER=$TIMESCALEDB_USER/g" ./.env
[ -z $TIMESCALEDB_PASSWORD ] || sed -i "s/DATABASE_PASSWORD=123456/DATABASE_PASSWORD=$TIMESCALEDB_PASSWORD/g" ./.env

# run the backend
$(pipenv --py) ./wsgi.py
