from flask import Flask

app = Flask(__name__)
app.secret_key = "secret_key"

from .login_service import *
from . import error_handling
from . import routes
