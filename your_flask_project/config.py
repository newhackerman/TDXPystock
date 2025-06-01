import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or         'mysql+pymysql://stock:!!@127.0.0.1/stock' # Default, user should change
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True # Change for production
