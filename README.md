# brewmaster-backend
Backend for brewmaster project.

## Installation

### Recommended requirements:

- [Python 3.7](https://www.python.org/downloads/)
- [Pipenv](https://github.com/pypa/pipenv)
- [PostgreSQL 11.5](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/downloads)

### Downloading code base

The Git installation example below will download the codebase project and run the pipenv install. Pipenv 
will create a virtual environment in which will install all project dependencies.

```
git clone https://github.com/brewmajsters/brewmaster-backend.git
cd brewmaster-backend
pipenv install
```

### Create environment variables file .env

- In project root is located file `.env.example`.
- Rename this file to `.env`.

### Setup postgres DB with timescale extension
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

Cheers! :beers:, by team **Brewmasters**.
