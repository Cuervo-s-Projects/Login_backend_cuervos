from app.utils import send_verification_email
from flask import url_for

def test_send_email_success(app, mail_outbox):
    token = "test-token"
    email = "test@example.com"

    with app.app_context():
        url = url_for('auth.verify_email', token=token, _external=True)
        success = send_verification_email(email=email, token=token)

    assert success is True
    assert len(mail_outbox) == 1
    assert email in mail_outbox[0].recipients
    assert token in mail_outbox[0].body
