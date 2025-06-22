from flask import url_for, current_app
from flask_mail import Mail, Message

from app.extensions import mail

def send_verification_email(email, token):
    try:
        with current_app.app_context(): 
            verification_url = url_for('auth.verify_email',
                                        token=token,
                                        _external=True)
            
        msg = Message('Verifica tu email', sender='noreply@demo.com', recipients=[email])
        msg.body = f'''Para verificar tu cuenta, visita: {verification_url}\n\nSi no solicitaste esto, ignora este email.'''
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error enviando email a {email}: {str(e)}")
        return False