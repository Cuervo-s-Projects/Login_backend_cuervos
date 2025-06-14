from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from app.routes import auth_bp
from app.video_routes import video_bp
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'ef(b$7lyx4-qjio((fcy!=c*ob0+k)b+m96o6ock=tc)ot@@ht'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

jwt = JWTManager(app)
CORS(app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            }
        }
    )

# Configuración de Swagger con seguridad JWT
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "securityDefinitions": {
        "JWT": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT token. Format: 'Bearer {token}'"
        }
    }
}

Swagger(app, config=swagger_config, template=swagger_template)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(video_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
