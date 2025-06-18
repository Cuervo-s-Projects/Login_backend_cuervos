from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from .service import UserService

from flasgger import swag_from

import os
import re

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/signup', methods=['POST'])
def sign_up():
    """
    Login de usuario
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
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
            password_confirm:
              type: string
              
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
        
        required_fields = ['username', 'email', 'password', 'password_confirm']
        if not all(field in data for field in required_fields):
            return jsonify({
              "message": "Required fields are missing"
            }),400

        if data['password'] != data['password_confirm']:
            return jsonify({
              "message": "Passwords do not match"
            }),400

        service = UserService()
        status = service.create_user(            
                email=data['email'],
                username=data['username'],
                password=data['password']
                )
        
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
    Login de usuario
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
            - password
          properties:
            username:
              type: string
            password:
              type: string
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
    data = request.get_json()
    email = data['email']
    password = data['password']

    service = UserService()
    user = service.authenticate(email=email, password=password)
    
    if not user:
      return jsonify({
            "message": "Incorrect user or password"
        }),401
    
    access_token = create_access_token(identity={
      "email": user.email,
      "username": user.username
    })

    response =  jsonify({
        "access_token": access_token
    })

    response.status_code = 200
    return response