import json
import logging
import uuid
from logging import Handler, Filter
from flask import request
from api import http_status
import core.models


class DBFilter(Filter):
    def filter(self, record):
        if hasattr(record, 'extra') and record.extra is not None:
            status_code = record.extra.get('status_code')
            if status_code:
                record.status_code = status_code
            else:
                record.status_code = http_status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            record.status_code = http_status.HTTP_500_INTERNAL_SERVER_ERROR
            record.extra = None

        if not hasattr(record, 'msg'):
            record.msg = 'No message provided'

        if request:
            record.request_body = (
                None if
                request.data is None
                or request.data is b''
                or request.data is b'{}'
                else json.loads(request.data)
            )
            record.method = request.method
            record.url = request.base_url
        else:
            record.request_body = None
            record.method = "None"
            record.url = "cron"

        return True


class DBHandler(Handler):
    def emit(self, record):
        try:
            Notification = core.models.notification.Notification
        except core.models.notification.Notification.DoesNotExist:
            from core.models import Notification

        Notification(
            message=record.msg,
            request=record.request_body,
            method=record.method,
            url=record.url,
            module=record.module,
            function=record.funcName,
            level=record.levelname,
            status_code=record.status_code,
            additional_data=record.extra
        ).create()


def init_logger():
    # Create a custom logger
    logger = logging.getLogger('root_logger')
    logger.setLevel('INFO')

    # Create handlers
    data_log = DBHandler()
    output_log = logging.StreamHandler()

    data_log.setLevel(logging.WARNING)
    output_log.setLevel(logging.DEBUG)

    data_log.addFilter(DBFilter())

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    data_log.setFormatter(formatter)
    output_log.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(data_log)
    logger.addHandler(output_log)

    logger = logging.getLogger()
    logger.setLevel('INFO')
