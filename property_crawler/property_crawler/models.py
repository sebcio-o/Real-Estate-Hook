from property_crawler import settings
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_items_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Property(DeclarativeBase):
    __tablename__ = "property"
    id = Column(Integer, primary_key=True)
    site = Column(String)
    thumbnail = Column(String)
    price = Column(Integer)
    link = Column(String, unique=True)
    title = Column(String)
    rooms = Column(Integer)
    address = Column(String)
