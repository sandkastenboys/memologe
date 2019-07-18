import os

from sqlalchemy.exc import DBAPIError
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from config import config

if config["sqlite"] == "True":
    engine = create_engine("sqlite:///" + os.path.join("./", "new_db"))
else:  # Mysql
    engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])

Session: sessionmaker = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()


session = Session()
connection = session.connection()


def reload() -> None:
    global Session, session, connection
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = session.connection()


def check_mysql_connection() -> None:
    if config["sqlite"] == "True":
        try:
            connection.scalar(select([1]))
            return
        except DBAPIError:  # FIXME put correct exception
            print("Connection Timeout")
        reload()
