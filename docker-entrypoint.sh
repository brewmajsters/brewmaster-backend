#!/bin/bash

# TimeScaleDB environment variables
[ -z $DATABASE_HOST ] || sed -i "s/DATABASE_HOST.*/DATABASE_HOST=$DATABASE_HOST/g" ./.env
[ -z $DATABASE_PORT ] || sed -i "s/DATABASE_PORT.*/DATABASE_PORT=$DATABASE_PORT/g" ./.env
[ -z $DATABASE_NAME ] || sed -i "s/DATABASE_NAME.*/DATABASE_NAME=$DATABASE_NAME/g" ./.env
[ -z $DATABASE_USER ] || sed -i "s/DATABASE_USER.*/DATABASE_USER=$DATABASE_USER/g" ./.env
[ -z $DATABASE_PASSWORD ] || sed -i "s/DATABASE_PASSWORD.*/DATABASE_PASSWORD=$DATABASE_PASSWORD/g" ./.env

# backend aplication environment variables
[ -z $SERVER_HOST ] || sed -i "s/SERVER_HOST.*/SERVER_HOST=$SERVER_HOST/g" ./.env
[ -z $SERVER_PORT ] || sed -i "s/SERVER_PORT.*/SERVER_PORT=$SERVER_PORT/g" ./.env
[ -z $RUN_ENVIRONMENT ] || sed -i "s/RUN_ENVIRONMENT.*/RUN_ENVIRONMENT=$RUN_ENVIRONMENT/g" ./.env
[ -z $SETTINGS_MODE ] || sed -i "s/SETTINGS_MODE.*/SETTINGS_MODE=$SETTINGS_MODE/g" ./.env

# MQTT environment variables
[ -z $MQTT_CLIENT_NAME ] || sed -i "s/MQTT_CLIENT_NAME.*/MQTT_CLIENT_NAME=$MQTT_CLIENT_NAME/g" ./.env
[ -z $MQTT_KEEPALIVE ] || sed -i "s/MQTT_KEEPALIVE.*/MQTT_KEEPALIVE=$MQTT_KEEPALIVE/g" ./.env
[ -z $MQTT_TIMEOUT ] || sed -i "s/MQTT_TIMEOUT.*/MQTT_TIMEOUT=$MQTT_TIMEOUT/g" ./.env
[ -z $BROKER_HOST ] || sed -i "s/BROKER_HOST.*/BROKER_HOST=$BROKER_HOST/g" ./.env
[ -z $BROKER_PORT ] || sed -i "s/BROKER_PORT.*/BROKER_PORT=$BROKER_PORT/g" ./.env

# run the backend
$(pipenv --py) ./wsgi.py
