from flask import Flask
from flask_cors import CORS
from config import Config
from datetime import timedelta
from app.extensions import mail, jwt, swagger
from app.routes import auth_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    #app.config["JWT_VERIFY_SUB"] = False

    mail.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    app.register_blueprint(auth_bp, url_prefix="/api")
    return app
