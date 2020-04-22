# brewmaster-backend
Backend for brewmaster project.

## Installation

### Requirements:

- [Python 3.7](https://www.python.org/downloads/)
- [Pipenv](https://github.com/pypa/pipenv)
- [PostgreSQL](https://www.postgresql.org/download/) (recommended version 11.5)
- [Git](https://git-scm.com/downloads)

### 1. Downloading code base

The Git installation example below will download the codebase project and run the pipenv install. Pipenv
will create a virtual environment in which will install all project dependencies.

```
git clone https://github.com/brewmajsters/brewmaster-backend.git
cd brewmaster-backend
pipenv install
```

### 2. Create environment variables file .env

- In project root is located file `.env.example`.
- Rename this file to `.env`.
- Configure variables in `.env` file according to your needs.

(Pay attention to variable: `RUN_ENVIRONMENT`. If you set that variable to value `development`,
this configuration setting will create software emulated modules for testing purposes.
This setting should be activated only if you can't communicate with real devices and HW components.
For production purposes you should set this variable to value `production`.)

### 3. Setup postgres DB with timescale extension
1. Download [PostgreSQL](https://www.postgresql.org/download/) (Our tested and working Postgresql server with timescale extension is version 11.5).
2. Install Postgresql according to manual on official web page.
3. Download [TimeScaleDB](https://docs.timescale.com/latest/getting-started/installation) extension for Postgresql.
4. Install TimeScaleDB according to manual on official web page.
5. Add TimeScale extension to installed Postgresql server.
   1. Connect to Postgresql server via CMD: `psql -U postgres -h host -p port`
   2. Create new database: `CREATE database tutorial;`
   3. Connect to created database: `\c tutorial`
   4. Create TimescaleDB extension to specified database: `CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;`

> **WARNING**: During installation on Windows platform creating database extension raised error:
> `ERROR: could not load library "C:/Program Files/PostgreSQL/11/lib/timescaledb-1.5.0.dll": The specified module could not be found.`
> Issue was resolved on [Github](https://github.com/timescale/timescaledb/issues/1398).

### 4. Activating environment and installing project dependencies

1. Activate environment `pipenv shell`.
2. Run download dependencies from pipfile `pipenv update`.

### 5. Populate DB with testing data

- If you only wish to create empty DB with no testing data skip this step.

1. Run server from project root path with command: `python wsgi.py` (only for DB table recreating purposes)
2. After the server start-up is finished, you need to look if DB tables are created successfully.
3. Stop the server.
4. Run command for populating DB tables with testing data: `flask seed run`

### 6. Project startup

1. Run command in project root `python wsgi.py`.

#### Dockerfile startup

**DEPENDENCY:** Running TimescaleDB instance as docker: [guide](https://github.com/brewmajsters/timescaledb-docker)

1. Build from the Dockerfile: `docker build -t backend:latest .`
2. Run the container from newly created image:
    - available environment variables: `TIMESCALEDB_HOST` `TIMESCALEDB_PORT` `TIMESCALEDB_NAME` `TIMESCALEDB_USER` `TIMESCALEDB_PASSWORD`
    - retrieve the timescaldb docker instance ip address: `docker inspect <TIMESCALEDB-DOCKER-ID> | jq -r '.[0].NetworkSettings.Networks.bridge.IPAddress'`
    - e.g. `docker run -d --name backend -p 5000:5000 -e TIMESCALEDB_HOST=<IP> -e TIMESCALEDB_PASSWORD=<PASSWD> backend`

## Implementation and Maintaining

- Project is developed in **python** with **flask** web micro-framework.

- Backend communicates with 4 ways:
    - Communication through REST.
    - Communication with PostgreSQL DB.
    - Communication through MQTT.
    - Communication through Web Sockets.

- We use strict code-style according to [PEP8](https://www.python.org/dev/peps/pep-0008/)
and we are using for maintaining codebase technique git-flow.
    - **master** branch always contains stable version of source code.
    - **develop** branch containing changes implemented in specific sprint.
    - **feature/** branches containing implementations of specific issues/features.
    - **fix/** branches containing error corrections.

#### Testing

Implemented tests are located in path `core/tests/*`. To run test file, its needed to name it with prefix `test_*.py`.
Tests are implemented with [pytest](https://github.com/pytest-dev/pytest/) library. Pytest settings are located in project root file `pytest.ini`.

- To run tests it's needed to type command `pytest`.

#### Seeding DB

Database seed is made with library [flask-seeder](https://github.com/diddi-/flask-seeder). All seeders are located in
path `seeds/*`

- To seed database with fake data for test purposes, its necessary to run command `flask seed run`.

Cheers! :beers:, by team **Brewmasters**.
