from app.repository import Repository
from app.models import User

from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app

class UserService:
    def __init__(self):
        self.repository = Repository()

    def create_user(self, email, username, password, last_name, first_name, age, date_birth):
        if self.repository.find_by_email(email=email.lower().strip()):
            return("Email already exists")
        
        if self.repository.find_by_username(username=username.strip()):
            return("Username already exists")

        hashed_password = generate_password_hash(str(password))
        user = User(username=username, email=email, password=hashed_password, last_name=last_name, first_name=first_name, age=age, date_birth=date_birth)
        errors = user.validate()
        if errors:
            return(errors)
                
        self.repository.create(user)
        
        return "OK"

    def authenticate(self, email, password):
        user = self.repository.find_by_email(email=email)
        if not user:
            return None
        if check_password_hash(user.password, str(password)):
            return user
        return None
    
    def generate_jwt_token(self, email, username):
        return create_access_token(identity={
        "email": email,
        "username": username
    })
    
    def get_by_email(self, email):
        user = self.repository.find_by_email(email=email)
        return user
    
    def update_user(self, user):
        self.repository.update(user=user)
        return True
    
    def generate_email_token(self, email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt='email-confirm-salt')
    
    def confirm_verification_token(self, token, expiration=None):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
            return email
        except SignatureExpired:
            return None
        except BadSignature:
            return None


