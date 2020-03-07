ARG PYTHON_VERSION=3.7

FROM python:${PYTHON_VERSION}-buster
MAINTAINER brewmasters

RUN pip install pipenv

ADD . /brewmaster-backend
WORKDIR /brewmaster-backend

RUN cp .env.example .env \
    && pipenv install

ENTRYPOINT ["./docker-entrypoint.sh"]
