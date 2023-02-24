from sqlalchemy.orm import Session
from .database import User, engine, Event

session = Session(engine)


def get_user_by_nickname(value: str):
    user = session.query(User).where(User.nickname == value).first()
    return user


def add_item_to_db(obj):
    session.add(obj)
    session.commit()


def get_events_for_current_user_by(date):
    events = session.query(Event).filter(Event.date == date, Event.user == 1).all()
    return events