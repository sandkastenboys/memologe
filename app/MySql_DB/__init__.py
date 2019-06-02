from config import config
import time
import random
import sqlite3
import os
from objects import *
from sqlalchemy import String, Integer, Column
from typing import Union

class Memes(Base):
    __tablename__ = "meme_list"

    uuid : Union[int,Column] = Column(Integer, autoincrement=True, primary_key=True)
    link : Union[str,Column] = Column(String(256), unique=True)
    rating : Union[int,Column]  = Column(Integer)
    post_time : Union[int,Column]  = Column(Integer)
    path: Union[int, Column] = Column(String(45))
    stealer : Union[str, Column] = Column(String(32))

    @staticmethod
    def create(link, path, stealer) -> 'Memes':

        meme : Memes = Memes(link = link, rating = 0, post_time=round(time.time()), path = path, stealer = stealer)

        session.add(meme)
        session.commit()

        return meme


class Tags(Base):
    __tablename__ = "tags"

    tag_uuid : Union[int, Column] = Column(Integer, autoincrement=True, primary_key= True)
    uuid : Union[int,Column] = Column(Integer, primary_key=False)
    tag : Union[str,Column] = Column(String(32), primary_key=False)

    @staticmethod
    def create(uuid : int, tag : str):

        tag : Tags = Tags(uuid = uuid, tag = tag)

        session.add(tag)
        session.commit()

        return tag

Base.metadata.create_all(engine)