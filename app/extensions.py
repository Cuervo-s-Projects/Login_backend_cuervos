from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flasgger import Swagger

mail = Mail()
jwt = JWTManager()
swagger = Swagger()
