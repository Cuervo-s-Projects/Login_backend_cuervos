from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app.utils import send_verification_email
from app.service import UserService


auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/signup', methods=['POST'])
def sign_up():
    """
    Signup user
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
            - password_confirm
            - last_name
            - first_name
            - age
            - date_birth
          properties:
            username:
              type: string
              example: luis
            email:
              type: string
              example: luis@gmail.com
            password:
              type: string
              example: 1234
            password_confirm:
              type: string
              example: 1234
            last_name:
              type: string
              example: luis
            first_name:
              type: string
              example: Gonzales
            age:
              type: string
              example: 20
            date_birth:
              type: date
              example: 2025-06-17T21:33:47.200+00:00
              
    responses:
      200:
        description: Usuario creado
        schema:
          type: object
          properties:
            message:
                type: string
                example: User successfully created
      400:
        description: Error en la creacion de usuario
    """
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
def login():
    """
    Login user
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: luis@gmail.com
            password:
              type: string
              example: 1234
    responses:
      200:
        description: Login exitoso
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Credenciales inválidas
    """
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
      
      access_token = service.generate_jwt_token(email=user.email, username=user.username)

      return jsonify({
          "access_token": access_token
      }), 200
    except Exception as e:
        return jsonify({
            "message": str(e)
        }),400
    

@auth_bp.route('/verify-email/<token>', methods=['GET'])
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