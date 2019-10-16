"""Routes for main pages."""
import logging
from flask import Blueprint

# Blueprint Configuration
blueprint = Blueprint('blueprint', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@blueprint.route('/test', methods=['GET'])
def test():
    logging.getLogger().error('test')
    return 'Tested'
