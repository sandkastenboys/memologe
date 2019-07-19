import os

from sqlalchemy.exc import DBAPIError, OperationalError
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from config import config


class DataBase:
    def __init__(self):

        if config["sqlite"] == "True":
            self.engine = create_engine("sqlite:///" + os.path.join("./", "new_db"))
        else:  # Mysql
            self.engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])

        self.Session: sessionmaker = sessionmaker(bind=self.engine)
        self.Base: DeclarativeMeta = declarative_base()

        self.session = self.Session()
        self.connection = self.session.connection()

    def reload(self) -> None:

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.connection = self.session.connection()

    def check_mysql_connection(self) -> None:
        if config["sqlite"] == "False":
            try:
                self.connection.scalar(select([1]))
                return
            except DBAPIError or OperationalError:  # FIXME put correct exception
                print("Connection Timeout")
            self.reload()


database_handler: DataBase = DataBase()
