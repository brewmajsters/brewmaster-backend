# brewmaster-backend
Backend for brewmaster project.

## Installation
This section describes setup requirements to run this project.

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
