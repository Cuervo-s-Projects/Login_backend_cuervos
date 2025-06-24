import pytest
from app import create_app
from app.extensions import mail as flask_mail

from flask import url_for
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "MAIL_SUPPRESS_SEND": True,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost:5000",
        "JWT_SECRET_KEY" : "test-secret",
    })

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mail_outbox(app):
    outbox = []

    def record_message(msg):
        outbox.append(msg)

    with patch.object(flask_mail, 'send', side_effect=record_message):
        yield outbox
