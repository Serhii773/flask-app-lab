import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    SECRET_KEY = 'super_secret_key_123'
    TEMPLATES_AUTO_RELOAD = True
    WTF_CSRF_ENABLED = True