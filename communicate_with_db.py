from sqlalchemy.orm import Session
from .database import User, engine

session = Session(engine)


def get_user_by_nickname(value: str):
    user = session.query(User).where(User.nickname == value).first()
    return user


def add_item_to_db(obj):
    session.add(obj)
    session.commit()

