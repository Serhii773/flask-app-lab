from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import views

from app.users import users_bp
from app.products import products_bp
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
