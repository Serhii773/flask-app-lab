from flask import Flask

app = Flask(__name__)
app.secret_key = "super_long_demo_secret_key_change_me"

from . import views