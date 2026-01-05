import os

class Config:
    """Application configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hackconrd2026-super-secret-key')

    # JWT settings - Intentionally weak for demo
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ALGORITHM = 'HS256'

    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'data/portal.db')

    # Upload/Documents path
    DOCUMENTS_PATH = os.environ.get('DOCUMENTS_PATH', 'data/documents')

    # Debug mode
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
