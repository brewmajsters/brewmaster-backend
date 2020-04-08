import logging
from core.models import Notification


class TestLogger:
    ERROR_MESSAGE = 'TEST_LOGGER'

    def test_logger(self, app):
        logging.getLogger('root_logger').error(self.ERROR_MESSAGE)
        logged_information = Notification.query.filter_by(message=self.ERROR_MESSAGE).first()

        assert logged_information.message == self.ERROR_MESSAGE
