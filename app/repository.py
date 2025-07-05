from app.models import User
from config.db import mongodb
from datetime import datetime
from bson import ObjectId

class Repository:
    
    def __init__(self):
        self.collection = mongodb['users']
    
    def create(self, user):
        user_data = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'age': user.age,
            'date_birth': user.date_birth, 
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'roles': user.roles,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'metadata': user.metadata,
        }
        result = self.collection.insert_one(user_data)
        return result
    
    def find_by_id(self, user_id):
        user_data = self.collection.find_one({'_id': ObjectId(user_id)})
        return User.from_dict(user_data) if user_data else None
    
    def find_by_email(self, email):
        user_data = self.collection.find_one({'email': email.lower().strip()})
        return User.from_dict(user_data) if user_data else None
    
    def find_by_username(self, username):
        user_data = self.collection.find_one({'username': username})
        return User.from_dict(user_data) if user_data else None
    
    def all_user(self):
        user_data = list(self.collection.find({}, {'_id': 0}))
        return user_data
    
    def update(self, user):
        user_data = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'age': user.age,
            'date_birth': user.date_birth,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'roles': user.roles,
            'created_at': user.created_at,
            'updated_at': datetime.now(),
            'metadata': user.metadata,
        }
        return self.collection.update_one(
            {'_id': user._id},
            {'$set': user_data}
        )
    
    def delete(self, user_id):
        return self.collection.delete_one({'_id': user_id})