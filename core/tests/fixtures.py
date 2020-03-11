import pytest
from application import create_app


@pytest.fixture
def app():
    app = create_app()
    return app
