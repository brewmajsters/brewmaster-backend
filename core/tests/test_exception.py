import pytest
from api import http_status
from api.errors import ApiException
from core.models import Notification
from core.tests.fixtures import app


class TestException:
    ERROR_MESSAGE = 'TEST_EXCEPTION'

    def test_api_exception(self, app):
        with pytest.raises(Exception) as exception:
            raise ApiException(self.ERROR_MESSAGE, status_code=http_status.HTTP_400_BAD_REQUEST)
        logged_information = Notification.query.filter_by(message=self.ERROR_MESSAGE).first()

        assert str(exception.value) == self.ERROR_MESSAGE
        assert logged_information.message == self.ERROR_MESSAGE
