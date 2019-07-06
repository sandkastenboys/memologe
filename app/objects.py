from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import select

from config import config
import os

if config["debug"] == "True":  # Sqlite3
    engine = create_engine('sqlite:///' + os.path.join("./", "new_db"))
else:  # Mysql
    print(config["SQLALCHEMY_DATABASE_URI"])
    engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])

Session: sessionmaker = sessionmaker(bind=engine)

Base: DeclarativeMeta = declarative_base()
session = Session()
connection = session.connection()


def reload():
    global Session, session, connection
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = session.connection()


def check_mysql_connection():
    try:
        connection.scalar(select([1]))
        return
    except:
        print("Connection Timeout")
    reload()
