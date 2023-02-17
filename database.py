from sqlalchemy import Column, Integer, Date, Time, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("sqlite:///app.db", echo=True)
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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    password = Column(String)


#create db if it doesnt exists
if not database_exists(engine.url):
    create_database(engine.url)


#create database
Base.metadata.create_all(engine)
