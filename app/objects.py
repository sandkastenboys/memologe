from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session
# from my_web_framework import get_current_request, on_request_end
from config import config
import os

engine = create_engine('sqlite:///' + os.path.join("./", "new_db"))
# create_engine(config["SQLALCHEMY_DATABASE_URI"])
Session: sessionmaker = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()
session = Session()

# Session = scoped_session(sessionmaker(bind=engine))

# @on_request_end
# def remove_session(req):
#   Session.remove()
