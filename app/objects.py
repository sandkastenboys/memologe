import os
import logging
from logging import Formatter, Handler, Logger

from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from config import config

logger: Logger = logging.Logger(__name__)
handler: Handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
format: Formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler.setFormatter(format)
logger.addHandler(handler)


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

        try:
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            self.connection = self.session.connection()
        except Exception:
            logger.critical("Can not reconnect to database", exc_info=True)

    def check_mysql_connection(self) -> None:
        if config["sqlite"] == "False":
            try:
                self.connection.scalar(select([1]))
                return
            except Exception:
                logger.error("Connection Timeout ... reconnecting")
            self.reload()


database_handler: DataBase = DataBase()
