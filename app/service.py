from app.repository import Repository
from app.models import User

from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def __init__(self):
        self.repository = Repository()

    def create_user(self, email, username, password):
        if self.repository.find_by_email(email=email.lower().strip()):
            return("Email already exists")
        
        if self.repository.find_by_username(username=username.strip()):
            return("Username already exists")

        hashed_password = generate_password_hash(password)
            
        user = User(username=username, email=email, password=hashed_password)
        errors = user.validate()
        if errors:
            return(errors)
        
        self.repository.create(user)
        return "OK"
    
    def authenticate(self, username, password):
        user = self.repository.find_by_username(username=username)
        if not user:
            return None
        if check_password_hash(user.password, password):
            return user
        return None
    
    def get_by_email(self, email):
        user = self.repository.find_by_email(email=email)
        return user



