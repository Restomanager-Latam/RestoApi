import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto')  

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'clave_jwt_por_defecto')  
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  
    CORS_ORIGINS = os.getenv("CORS_ORIGINS","*").split(",")
    CORS_METHODS = os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE").split(",")