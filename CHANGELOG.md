## 0.1.0: 06.11.2019

- **Feature**: Implemented timescale extension.

## 0.2.0: 18.11.2019

- **Feature**: Implemented communication via Web-Sockets.

## 0.3.0: 22.11.2019

- **Feature** Implemented testing sensors simulating real sensor MQTT message publishing.
- **Feature**: Implemented multiprocessing handling of more than one testing sensor.
- **Feature**: Created DB models according to specified ER diagram.

## 0.3.1: 04.12.2019

- **Fix**: Changed sensor.run() to sensor.stop() on disconnect client from socketio.

## 0.4.0: 25.02.2020

- **Feature**: Implemented basic unit tests via pytest.
- **Fix**: Changed language to raised exception messages.

## 0.5.0: 08.04.2020

- **Feature**: Implemented all REST endpoints.
- **Feature**: Implemented testing DB seed.
- **Feature**: Implemented communication with modules via MQTT according to MQTT API specification.
- **Change**: Changed Sensor emulator according to MQTT specification.

## 0.6.0: 22.04.2020

- **Feature**: Implemented mqtt ack message blocker.
- **Feature**: Added new env variables to .env.example file.
- **Feature**: Implemented possibility to change project environment.
- **Change**: Deleted testing and unused endpoints.
- **Change**: Deleted unused testing templates and static files.
- **Change**: Made changes in README.md file according to new configuration possibilities.
- **Change**: Changed format of parsing data according to MQTT API docs.
- **Change**: Changed Sensor model to ModuleNotification.
- **Fix**: Fixed setting value to device (distinction between module and device).

## 0.7.0: 03.05.2020

- **Feature**: Added devices list to module list/get endpoint.
- **Fix**: Fixed bad parsing string in emulator in set_module_value endpoint.
- **Change**: Changed channel name in socketio.

## 0.7.1: 06.05.2020

- **Feature**: Added datapoints to module structure.
- **Fix**: Renamed data_point attribute to datapoint in set_device endpoint.
- **Fix**: The device_uuid argument has since now uuid attribute of device not id.
- **Fix**: Added check for datapoint id (if exist) in set_device endpoint.

## 0.7.2: 10.05.2020

- **Feature**: Implemented set_config endpoint.
- **Fix**: Fixed topics to subscribe and publish.
- **Fix**: Fixed emulators with changed topics.
- **Fix**: Fixed parsing emulator set_value data.
