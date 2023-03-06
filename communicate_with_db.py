import datetime
import json
from sqlalchemy.orm import Session
from .database import User, engine, Event

session = Session(engine)


def create_json_from(object):
    event_dict = object.__dict__

    # Видаляємо ключ "_sa_instance_state", який додає SQLAlchemy
    event_dict.pop('_sa_instance_state', None)

    #Перетворюємо дату та час на рядки, щоб повернути їх користувачу
    event_dict['time'] = event_dict['time'].strftime('%H:%M')
    event_dict['date'] = event_dict['date'].strftime('%Y-%m-%d')

    json_string = json.dumps(event_dict)
    return json_string


def get_user_by_nickname(value: str):
    user = session.query(User).where(User.nickname == value).first()
    return user


def add_item_to_db(obj):
    session.add(obj)
    session.commit()


def get_events_for_current_user_by(date: datetime.date, user: int):
    events = session.query(Event).filter(Event.date == date, Event.user == user).all()
    jsonified_events = []
    for event in events:
        print(event)
        jsonified_events.append(create_json_from(event))
    return jsonified_events
