from uuid import uuid4
from config import config
from sqlalchemy import func, select
import requests
import shutil
from db_models import Memes, Tags, Association, User, Ratings
from typing import List, Union, NoReturn
from objects import session
from datetime import datetime
from func.static import resolve_platform

def prep4post(meme: Memes) -> str:
    user: User = id2user(meme.stealer)
    return 'Here your meme posted by: ' + str(user.username) + ' id = ' + str(meme.id) + ' : ' + ";".join(
        query_tags(meme.id)) + " " + meme.link


def query_tags(meme_id: int) -> List[str]:
    return_list = []
    for x in session.query(Tags).filter(Association.meme_id == meme_id, Tags.id == Association.tag_id).all():
        return_list.append(x.tag)
    return return_list


def parse_amount(string: str) -> int:
    if string == "":
        how_many = 1
    else:
        try:
            how_many: int = int(string)
        except:
            how_many: int = 1
    return how_many


def random_meme() -> Union[Memes, str]:
    meme: Memes = session.query(Memes).order_by(func.random()).first()

    if meme is None:
        return "There are 0 memes in the database"

    return meme


def yield_random_meme(message: str) -> str:
    try:
        how_many: int = int(message.split(" ")[1])
        if how_many > 10:
            how_many: int = 10
    except:
        how_many: int = 1

    for x in range(how_many):
        meme: Memes = random_meme()
        yield prep4post(meme)


def post_meme(link: str, tags: str, author: str, platform: int, posted_at: datetime) -> str:
    if not check_existens(link) and type(find_link(link)) is str:

        author_uuid: int = check_auther_registerd(author, platform)

        if config["save_memes_to_disc"] == "True":
            filename = download(link)
        else:
            filename = ""

        cm: Memes = Memes.create(link, filename, author_uuid, posted_at)

        if tags != "":

            tags: list = tags.split(";")

            for tag in tags:
                tag_id: int = create_tag(tag)
                create_association(tag_id, cm.id, author_uuid)

        return "Thx for your Meme"
    else:

        return "This Meme already got posted"


def create_tag(tag: str) -> int:
    db_tag: Tags = session.query(Tags).filter_by(tag=tag).first()

    if db_tag is None:
        return Tags.create(tag).id
    else:
        return db_tag.id


def create_association(tag_id: int, meme_id: int, user: int) -> 'Association':
    assoc: List[Association] = session.query(Association).filter_by(tag_id=tag_id, meme_id=meme_id).first()
    if assoc is None:
        return Association.create(meme_id, tag_id, user)


def download(link: str) -> str:
    filename = str(uuid4()) + "." + link.split(".")[-1]
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        try:
            try:
                with open(config["destination"] + filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            except:
                filename = str(uuid4()) + ".und"
                with open(config["destination"] + filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        except:
            print("Probebly no file behind:", link)
    return filename


def check_existens(link: str) -> bool:
    meme: Memes = session.query(Memes).filter_by(link=link).first()

    return meme is not None


def check_for_link(link) -> bool:
    return "http" in link.content


def find_link(post: str) -> Union[str, bool]:
    try:
        ind = post.index("http")
        temp = post[ind:].split(" ")
        return temp[0]
    except:
        return False


def check_auther_registerd(author_name: str, platform: int) -> int:
    author: User = session.query(User).filter_by(username=author_name, platform=platform).first()

    if author is None:
        u: User = User.create(platform, author_name)
        u.new_post()
        return u.user_id
    else:
        author.new_post()
        return author.user_id


def categorise_meme(meme_id: int, tags: str, author: str, platform: int) -> NoReturn:
    auther_uuid: int = check_auther_registerd(author, platform)

    cm: Memes = session.query(Memes).filter(Memes.id == int(meme_id)).first()

    if tags != "":

        tags: list = tags.split(";")

        for tag in tags:
            tag_id: int = create_tag(tag)
            create_association(tag_id, cm.id, auther_uuid)


def list_tags() -> str:
    ret_val: str = ""
    for tag in session.query(Tags.tag).all():
        ret_val += "\n" + tag[0]
    return ret_val


def list_users() -> str:
    ret_val: str = ""
    u: List[User] = session.query(User).order_by(User.posts.desc()).all()
    ret_val += "username" + " " * 12 + "platform" + " " * 12 + "interactions" + " " * 8
    for x in range(min(len(u), 10)):
        ret_val += "\n" + u[x].username + " " * (20 - len(u[x].username)) + str(resolve_platform[u[x].platform]) + " " * (
                20 - len(str(resolve_platform[u[x].platform]))) + str(u[x].posts)
    return ret_val


def history(meme_id: str) -> str:
    ret_val: str = ""

    meme: Memes = session.query(Memes).filter(Memes.id == int(meme_id)).first()

    if meme is None:
        return "Sorry there is no meme with this id yet"

    user: User = id2user(meme.stealer)
    ret_val += "```\nPosted by: " + str(user.username) + "\nTime: " + str(meme.post_time) + "\nRating: " + str(
        sum_ratings(meme.id)) + "\n\n"
    ret_val += "Tag / Vote" + " " * 10 + "User" + " " * 16 + "Time\n\n"

    tags = session.query(Tags, Association, User).filter(Association.meme_id == int(meme_id),
                                                         Association.tag_id == Tags.id,
                                                         Association.added_by == User.user_id)
    ratig = session.query(Ratings, User).filter(int(meme_id) == Ratings.meme_id,
                                                Ratings.added_by == User.user_id)

    time_line = sort_by_data(tags, ratig)

    for x in time_line:
        if x[0] != 0:
            ret_val += str(x[0].tag) + " " * (20 - len(x[0].tag)) + str(x[2].username) + " " * (
                    20 - len(str(x[2].username))) + str(x[1].time_added.strftime("%Y-%m-%d %H:%M:%S")) + "UTC Time\n"
        else:
            ret_val += rate2text(x[1].rate) + " " * (20 - len(rate2text(x[1].rate))) + str(x[2].username) + " " * (
                    20 - len(str(x[2].username))) + str(x[1].time_added.strftime("%Y-%m-%d %H:%M:%S")) + "UTC Time\n"
    #
    ret_val += "```"

    return ret_val


def rate2text(vote: int) -> str:
    if vote == 1:
        return "__upvote__"
    else:
        return "__downvote__"


def sort_by_data(tags, rating) -> list:
    data = []
    for rat, use in rating:
        print(rat.added_by, use.user_id, use.username)
        data.append((0, rat, use))
    data += tags
    data.sort(key=lambda date: datetime.strptime(str(date[1].time_added), "%Y-%m-%d %H:%M:%S"))
    return data


def rate_meme(meme_id: int, rate: int, user: str, platform: int) -> NoReturn:
    author_uuid: int = check_auther_registerd(user, platform)

    rat: Ratings = session.query(Ratings).filter(Ratings.added_by == author_uuid, Ratings.meme_id == meme_id).first()

    if rat is None:
        Ratings.create(author_uuid, meme_id, rate)


def sum_ratings(meme_id: int) -> int:
    sum_rat: int = 0
    for x in session.query(Ratings).filter(Ratings.meme_id == meme_id).all():
        sum_rat += x.rate
    return sum_rat


def id2user(user_id: int) -> 'User':
    return session.query(User).filter(User.user_id == user_id).first()


def id2meme(meme_id: int) -> str:
    meme = session.query(Memes).filter(Memes.id == meme_id).first()
    if meme is None:
        return "There is no meme with this id"
    else:
        return prep4post(meme)
