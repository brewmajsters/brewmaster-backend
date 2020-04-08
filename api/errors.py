import logging
from flask import jsonify
from api import http_status
from mqtt.errors import MQTTException


def register_error_handlers(app):
    @app.errorhandler(ApiException)
    def handle_invalid_usage(error):
        response = jsonify(error.payload)
        response.status_code = error.status_code
        return response

    @app.errorhandler(ValidationException)
    def handle_invalid_usage(error):
        response = jsonify(error.payload)
        response.status_code = error.status_code
        return response

    @app.errorhandler(MQTTException)
    def handle_invalid_usage(error):
        response = jsonify(error.payload)
        response.status_code = error.status_code
        return response


class ApiException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        details=None,
        previous=None,
        extra: dict = None
    ):
        super().__init__(message)
        self._status_code = status_code
        self._message = message
        self._details = details
        self._previous = previous
        self._extra = {"status_code": self.status_code}

        if extra:
            self._extra.update(extra)

        logging.getLogger('root_logger').error(self.message, extra={"extra": self._extra})

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def details(self):
        return self._details

    @property
    def previous(self):
        return self._previous

    @property
    def payload(self) -> dict:
        result = {
            'message': self.message,
        }

        if self.details:
            result['details'] = self.details

        return result


class ValidationException(Exception):
    def __init__(self, errors):
        super().__init__('Validation error')
        self._errors = errors
        self._status_code: int = http_status.HTTP_400_BAD_REQUEST

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def payload(self) -> dict:
        return self._errors
