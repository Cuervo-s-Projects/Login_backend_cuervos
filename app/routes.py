from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
import os 

from app.utils import send_verification_email
from app.service import UserService

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
swagger_path = os.path.join(root_path, "docs")

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/signup', methods=['POST'])
@swag_from(os.path.join(swagger_path, 'signup.yaml'))
def sign_up():
    try:
        data = request.get_json()
        required_fields = ['username', 'email', 'password', 'password_confirm', 'last_name', 'first_name', 'age', 'date_birth']
        if not all(field in data for field in required_fields):
            return jsonify({
              "message": "Required fields are missing"
            }),400

        if data.get('password') != data.get('password_confirm'):
            return jsonify({
              "message": "Passwords do not match"
            }),400
        
        service = UserService()
        status = service.create_user(            
                email=data.get('email'),
                username=data.get('username'),
                password=data.get('password'),
                last_name=data.get('last_name'),
                first_name=data.get('first_name'),
                age=data.get('age'),
                date_birth=data.get('date_birth')
                )
        
        token = service.generate_email_token(data.get('email'))
        send = send_verification_email(email=data.get('email'), token=token)

        if status == "OK":
          return jsonify({
              "message": "User successfully created"
          }),201
        
        return jsonify({
              "message": status
          }),400

    
    except Exception as e:
        return jsonify({
            "message": str(e)
        }),400


@auth_bp.route('/login', methods=['POST'])
@swag_from(os.path.join(swagger_path, 'login.yaml'))   
def login():
    try:
      data = request.get_json()

      if not data or 'email' not in data or 'password' not in data:
            return jsonify({"message": "Email and password are required"}), 400
      
      email = data.get('email')
      password = data.get('password')

      service = UserService()
      user = service.authenticate(email=email, password=password)
      
      if not user:
        return jsonify({
              "message": "Incorrect user or password"
          }),401
      
      access_token = service.generate_jwt_token(email=user.email)

      return jsonify({
          "access_token": access_token
      }), 200
    except Exception as e:
        return jsonify({
            "message": str(e)
        }),400
    

@auth_bp.route('/verify-email/<token>', methods=['GET'])
@swag_from(os.path.join(swagger_path, 'verify_email.yaml')) 
def verify_email(token):
  try:
    service = UserService()
    email = service.confirm_verification_token(token)
    if email is None:
       return jsonify({
              "message": "Incorrect token"
          }),401
    
    user = service.get_by_email(email)
    user.is_verified = True
    status = service.update_user(user)
    return jsonify({"message": "Email verificado con éxito"}), 200
  except Exception as e:
    return jsonify({"message": str(e)}), 400
  

@auth_bp.route('/profile', methods=['GET']) 
@jwt_required()
@swag_from(os.path.join(swagger_path, 'profile.yaml')) 
def profile():
  try:
    identity = get_jwt_identity()
    service = UserService()
    user = service.get_by_email(identity)
    user._id = str(user._id)

    return jsonify({
        "_id": str(user._id),
        "username": user.username,
        "age": user.age,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_birth": user.date_birth,
    }), 200
  except Exception as e:
    return jsonify({
        "message": str(e)
    }), 400
  
@auth_bp.route('/type_user', methods=['GET']) 
@jwt_required()
@swag_from(os.path.join(swagger_path, 'type_user.yaml')) 
def type_user():
  try:
    identity = get_jwt_identity()
    service = UserService()
    user = service.get_by_email(identity)

    return jsonify({
        "roles": user.roles
    }), 200
  except Exception as e:
    return jsonify({
        "message": str(e)
    }), 400
  
@auth_bp.route('/username', methods=['POST']) 
@swag_from(os.path.join(swagger_path, 'username.yaml')) 
def username():
  try:
    data = request.get_json()
    id = data.get('id')
    service = UserService()
    user = service.get_by_id(id)

    if user == None: 
      return jsonify({
        "message": "User not found"
      }), 401

    username = user.username

    return jsonify({
        "username": username
    }), 200
  except Exception as e:
    return jsonify({
        "message": str(e)
    }), 400
  
