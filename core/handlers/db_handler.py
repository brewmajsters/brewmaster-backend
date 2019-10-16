import datetime
import json
import logging
from logging import Handler, Filter

from flask import request

from api import http_status
import core.models
from application import db


class DBFilter(Filter):
    def filter(self, record):
        if hasattr(record, 'extra'):
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
                request.json is None
                or request.json is b''
                or request.json is b'{}'
                else json.loads(request.json)
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

        notification = Notification(
            message=record.msg,
            request=record.request_body,
            method=record.method,
            url=record.url,
            module=record.module,
            function=record.funcName,
            level=record.levelname,
            status_code=record.status_code,
            additional_data=record.extra
        )
        db.session.add(notification)
        db.session.commit()


def init_logger():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()
    logger.setLevel('INFO')

    data_log = DBHandler()
    data_log.setLevel('WARNING')
    data_log.addFilter(DBFilter())

    output_log = logging.StreamHandler()
    output_log.setLevel(logging.DEBUG)

    data_log.setFormatter(formatter)
    output_log.setFormatter(formatter)

    logger.addHandler(data_log)
    logger.addHandler(output_log)
