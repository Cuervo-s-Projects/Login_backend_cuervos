from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from app.routes import auth_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SWAGGER'] = {
    'title': 'Login Service Educarural',
    'uiversion': 3
}

Swagger(app)
app.register_blueprint(auth_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
