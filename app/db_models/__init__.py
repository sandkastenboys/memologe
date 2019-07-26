from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from objects import database_handler


class User(database_handler.Base):  # type: ignore
    __tablename__ = "user"

    platform: Union[int, Column] = Column(Integer)  # 0 -> Discord, 1 -> Telegram ... maybe other platforms added later
    user_id: Union[int, Column] = Column(Integer, autoincrement=True, primary_key=True)
    username: Union[str, Column] = Column(String(32))
    posts: Union[int, Column] = Column(Integer)  # Could be counted but we want to save performance

    @staticmethod
    def create(platform: int, username: str) -> "User":
        user: User = User(platform=platform, username=username[:32], posts=0)
        database_handler.session.add(user)
        database_handler.session.commit()
        return user

    def new_post(self):
        self.posts += 1
        database_handler.session.add(self)
        database_handler.session.commit()


class Memes(database_handler.Base):  # type: ignore
    __tablename__ = "meme_list"

    id: Union[int, Column] = Column(Integer, autoincrement=True, primary_key=True)
    link: Union[str, Column] = Column(String(512), unique=True)
    post_time: Union[datetime, Column] = Column(DateTime)
    path: Union[int, Column] = Column(String(45))
    stealer: Union[int, Column] = Column(Integer, ForeignKey("user.user_id"))

    @staticmethod
    def create(link, path, stealer, post_time=None) -> "Memes":
        if post_time is None:
            post_time = datetime.utcnow()

        meme: Memes = Memes(link=link[:512], post_time=post_time, path=path[:45], stealer=stealer)

        database_handler.session.add(meme)
        database_handler.session.commit()

        return meme


class Tags(database_handler.Base):  # type: ignore
    __tablename__ = "tags"

    id: Union[int, Column] = Column(Integer, autoincrement=True, primary_key=True)
    tag: Union[str, Column] = Column(String(32), unique=True)

    @staticmethod
    def create(a_tag: str):
        tag: Tags = Tags(tag=a_tag)

        database_handler.session.add(tag)
        database_handler.session.commit()

        return tag


class Association(database_handler.Base):  # type: ignore
    __tablename__ = "association"
    meme_id: Union[int, Column] = Column(Integer, ForeignKey("meme_list.id"), primary_key=True)
    tag_id: Union[int, Column] = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    added_by: Union[int, Column] = Column(Integer, ForeignKey("user.user_id"))
    time_added: Union[datetime, Column] = Column(DateTime)

    @staticmethod
    def create(meme_id: int, tag_id: int, user: int) -> "Association":
        ass = Association(meme_id=meme_id, tag_id=tag_id, added_by=user, time_added=datetime.now())

        database_handler.session.add(ass)
        database_handler.session.commit()

        return ass


class Ratings(database_handler.Base):  # type: ignore
    __tablename__ = "ratings"
    meme_id: Union[int, Column] = Column(Integer, ForeignKey("meme_list.id"), primary_key=True)
    added_by: Union[int, Column] = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    rate: Union[int, Column] = Column(Integer)
    time_added: Union[datetime, Column] = Column(DateTime)

    @staticmethod
    def create(user: int, meme: int, vote: int):
        v: Ratings = Ratings(meme_id=meme, added_by=user, rate=vote, time_added=datetime.now())

        database_handler.session.add(v)
        database_handler.session.commit()

        return v


database_handler.Base.metadata.create_all(database_handler.engine)  # type: ignore
