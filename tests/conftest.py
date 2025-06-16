import pytest
from flask import Flask

@pytest.fixture(scope="module")
def test_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret'
    app.config['WTF_CSRF_ENABLED'] = False  # Desactiva CSRF para pruebas
    with app.app_context():
        yield app
