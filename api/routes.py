"""Routes for main pages."""
import logging
from flask import Blueprint, request

# Blueprint Configuration
from api import http_status
from core.errors import ApiException

blueprint = Blueprint('blueprint', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@blueprint.route('/log_test', methods=['GET'])
def log_test():
    logging.getLogger().error('test')
    return 'Tested'


@blueprint.route('/exception_test', methods=['GET'])
def exception_test():
    raise ApiException('Test exception', status_code=http_status.HTTP_403_FORBIDDEN)
