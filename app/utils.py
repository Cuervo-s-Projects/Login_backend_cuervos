import jwt
import os
from werkzeug.security import check_password_hash

def verify_password(password_plain, password_hashed):
    return check_password_hash(password_hashed, password_plain)

def generate_token(email):
    payload = {'email': email}
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm='HS256')
