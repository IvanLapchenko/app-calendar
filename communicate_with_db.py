from sqlalchemy import select
from sqlalchemy.orm import Session
from database import User, engine

session = Session(engine)


def get_user_by_nickname(value: any):
    user = select(User).where(User.nickname == value)
    return user


def add_item_to_db(obj):
    session.add(obj)
    session.commit()