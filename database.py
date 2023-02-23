from sqlalchemy import Column, Integer, Date, Time, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from flask_login import UserMixin


engine = create_engine("sqlite:///app.db?check_same_thread=False", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date)
    time = Column("time", Time, nullable=True)
    header = Column("header", String(80))
    describe = Column("describe", String(240), nullable=True)

    def __init__(self, date, time, header, describe):
        super().__init__()
        self.date = date
        self.time = time
        self.header = header
        self.describe = describe


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, nickname, email, password):
        super().__init__()
        self.nickname = nickname
        self.email = email
        self.password = password


#create db if it doesnt exists
if not database_exists(engine.url):
    create_database(engine.url)


#create database
Base.metadata.create_all(engine)
