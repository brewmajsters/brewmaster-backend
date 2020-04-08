import logging
from mqtt import mqtt_status


class MQTTException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = mqtt_status.MQTT_ERR_UNKNOWN,
    ):
        super().__init__(message)
        self._status_code = status_code
        self._message = message
        self._extra = {'status_code': self.status_code}

        logging.getLogger('root_logger').error(self.message, extra={'extra': self._extra})

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def payload(self) -> dict:
        result = {
            'message': self.message,
            'status_code': self.status_code
        }

        return result
