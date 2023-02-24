from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret_key"
CORS(app)

from .login_service import *
from . import routes
