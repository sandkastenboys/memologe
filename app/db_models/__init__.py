import datetime
from objects import Base, engine, session
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from typing import Union


class User(Base):
    __tablename__ = "user"

    platform: Union[bool, int] = Column(Integer)  # 0 -> Discord, 1 -> Telegram ... maybe other platforms added later
    user_id: Union[int, Column] = Column(Integer, autoincrement=True, primary_key=True)
    username: Union[str, Column] = Column(String(32))
    posts: Union[int, Column] = Column(Integer)  # Could be counted but we want to save performance

    @staticmethod
    def create(platform: int, username: str) -> 'User':
        user: User = User(platform=platform, username=username, posts=0)
        session.add(user)
        session.commit()
        return user

    def new_post(self):
        self.posts += 1
        session.add(self)
        session.commit()


class Memes(Base):
    __tablename__ = "meme_list"

    id: Union[int, Column] = Column(Integer, autoincrement=True, primary_key=True)
    link: Union[str, Column] = Column(String(512), unique=True)
    post_time: Union[datetime.datetime, Column] = Column(DateTime)
    path: Union[int, Column] = Column(String(45))
    stealer: Union[int, Column] = Column(Integer, ForeignKey('user.user_id'))

    @staticmethod
    def create(link, path, stealer, post_time=None) -> 'Memes':
        if post_time is None:
            post_time = datetime.datetime.utcnow()

        meme: Memes = Memes(link=link, post_time=post_time, path=path, stealer=stealer)

        session.add(meme)
        session.commit()

        return meme


class Tags(Base):
    __tablename__ = "tags"

    id: Union[int, Column] = Column(Integer, autoincrement=True, primary_key=True)
    tag: Union[str, Column] = Column(String(32), unique=True)

    @staticmethod
    def create(a_tag: str):
        tag: Tags = Tags(tag=a_tag)

        session.add(tag)
        session.commit()

        return tag


class Association(Base):
    __tablename__ = 'association'
    meme_id: Union[int, Column] = Column(Integer, ForeignKey('meme_list.id'), primary_key=True)
    tag_id: Union[int, Column] = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    added_by: Union[int, Column] = Column(Integer, ForeignKey('user.user_id'))
    time_added: Union[datetime.datetime, Column] = Column(DateTime)

    @staticmethod
    def create(meme_id: int, tag_id: int, user: int) -> 'Association':
        ass = Association(meme_id=meme_id, tag_id=tag_id, added_by=user, time_added=datetime.datetime.now())

        session.add(ass)
        session.commit()

        return ass


class Ratings(Base):
    __tablename__ = "ratings"
    meme_id: Union[int, Column] = Column(Integer, ForeignKey('meme_list.id'), primary_key=True)
    added_by: Union[int, Column] = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    rate: Union[int, Column] = Column(Integer)
    time_added: Union[datetime.datetime, Column] = Column(DateTime)

    @staticmethod
    def create(user: int, meme: int, vote: int):
        v: Ratings = Ratings(meme_id=meme, added_by=user, rate=vote, time_added=datetime.datetime.now())

        session.add(v)
        session.commit()

        return v


Base.metadata.create_all(engine)
