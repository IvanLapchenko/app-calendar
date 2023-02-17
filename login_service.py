from sqlalchemy import select
from database import User
from . import app
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


def get_user_by_nickname(value: any):
    user = select(User).where(User.nickname == value)
    return user if user else None


@login_manager.user_loader
def load_user(user_id):
    return select(User).where(User.id == user_id)

