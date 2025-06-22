from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='secret')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='jwt-secret')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')

    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'