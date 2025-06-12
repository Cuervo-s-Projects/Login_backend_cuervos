from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from app.routes import auth_bp
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'ef(b$7lyx4-qjio((fcy!=c*ob0+k)b+m96o6ock=tc)ot@@ht'

jwt = JWTManager(app)
CORS(app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.1.0:3000"],
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            }
        }
    )
Swagger(app)

app.register_blueprint(auth_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
