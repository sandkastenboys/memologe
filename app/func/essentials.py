import shutil
from datetime import datetime
from typing import Iterator, List, Tuple, Union
from uuid import uuid4

import emoji
import requests
from sqlalchemy import func

from config import config
from db_models import Association, Memes, Ratings, Tags, User
from func.static import resolve_platform
from objects import database_handler, logger


def prep4post(meme: Memes) -> str:
    user: User = id_to_user(meme.stealer)

    msg: str = "Here is meme number {}".format(meme.id)
    tags: List[str] = query_tags(meme.id)
    if tags:
        msg += " with tags {}".format(";".join(tags))
    msg += "originaly posted by {}\n{}".format(user.username, meme.link)
    return msg


def query_tags(meme_id: int) -> List[str]:
    return_list: List[str] = []
    for x in (
        database_handler.session.query(Tags).filter(Association.meme_id == meme_id, Tags.id == Association.tag_id).all()
    ):
        return_list.append(x.tag)
    return return_list


def parse_amount(string: str) -> int:
    how_many: int = 0
    if string == "":
        how_many = 1
    else:
        try:
            how_many = int(string)
        except ValueError:
            how_many = 1
    return how_many


def random_meme() -> Union[Memes, str]:
    if config["sqlite"] == "True":  # DB manager dialect depending
        random = func.random()
    else:
        random = func.rand()
    meme: Memes = database_handler.session.query(Memes).order_by(random).first()

    if meme is None:
        return "There are 0 memes in the database"

    return meme


def yield_random_meme(count: int) -> Iterator[str]:
    for _ in range(min(config["max_post"], count)):
        meme: Memes = random_meme()
        yield prep4post(meme)


def add_meme(link: str, tags: str, author: str, platform: int, posted_at: datetime) -> str:
    if not check_existens(link) and type(find_link(link)) is str:

        author_uuid: int = check_auther_registerd(author, platform)

        if config["save_memes_to_disc"] == "True":
            filename = download(link)
        else:
            filename = ""

        cm: Memes = Memes.create(link, filename, author_uuid, posted_at)

        if not tags:
            tag_list: list = tags.split(";")

            for tag in tag_list:
                tag_id: int = create_tag(tag)
                create_association(tag_id, cm.id, author_uuid)

        return "Thx for your Meme"
    else:
        return "This Meme already got posted"


def create_tag(tag: str) -> int:
    db_tag: Tags = database_handler.session.query(Tags).filter_by(tag=tag).first()

    if db_tag is None:
        return Tags.create(tag).id
    else:
        return db_tag.id


def create_association(tag_id: int, meme_id: int, user: int):
    assoc: List[Association] = database_handler.session.query(Association).filter_by(
        tag_id=tag_id, meme_id=meme_id
    ).first()
    if assoc is None:
        return Association.create(meme_id, tag_id, user)
    else:
        return None


def download(link: str) -> str:
    filename: str = str(uuid4()) + "." + link.split(".")[-1]
    try:
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            try:
                try:
                    with open("{}{}".format(config["destination"], filename), "wb") as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                except IOError:
                    filename = str(uuid4()) + ".und"
                    with open("{}{}".format(config["destination"], filename), "wb") as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
            except IOError:
                logger.error("Probably no file behind %s", link)
        return filename
    except Exception:
        logger.error("SSL Signature Wrong Skiping this meme")

    # Returns Empty string when something went wrong
    return ""


def check_existens(link: str) -> bool:
    meme: Memes = database_handler.session.query(Memes).filter_by(link=link).first()

    return meme is not None


def check_for_link(link) -> bool:
    return "http" in link.content


def find_link(post: str) -> Union[str, bool]:
    try:
        ind: int = post.index("http")
        temp: List[str] = post[ind:].split(" ")
        return temp[0]
    except ValueError:
        return False


def check_auther_registerd(author_name: str, platform: int) -> int:
    author: User = database_handler.session.query(User).filter_by(username=author_name, platform=platform).first()

    if author is None:
        logger.info("created user %s on platform %s", author_name, platform)

        u: User = User.create(platform, author_name)
        u.new_post()
        return u.user_id
    else:
        author.new_post()
        return author.user_id


def categorise_meme(meme_id: int, tags: str, author: str, platform: int) -> None:
    author_uuid: int = check_auther_registerd(author, platform)

    meme: Memes = database_handler.session.query(Memes).filter(Memes.id == int(meme_id)).first()

    if tags != "":

        tags_list: list = tags.split(";")

        for tag in tags_list:
            tag_id: int = create_tag(tag)
            create_association(tag_id, meme.id, author_uuid)


def list_tags() -> str:
    ret_val: str = ""
    for tag in database_handler.session.query(Tags.tag).all():
        ret_val += "\n" + tag[0]
    return ret_val


def list_users() -> str:
    u: List[User] = database_handler.session.query(User).order_by(
        User.posts.desc()  # type: ignore
    ).all()
    ret_val: str = "```Username" + " " * 12 + "Platform" + " " * 12 + "Interactions" + " " * 8
    for x in range(min(len(u), 10)):
        user: str = u[x].username
        platform: str = resolve_platform[u[x].platform]
        ret_val += "\n{}{}{}{}{}".format(user, " " * (20 - len(user)), platform, " " * (20 - len(platform)), u[x].posts)
    ret_val += "```"
    return ret_val


def history(meme_id: int) -> str:
    meme: Memes = database_handler.session.query(Memes).filter(Memes.id == meme_id).first()

    if meme is None:
        return "Sorry there is no meme with this id yet"

    user: User = id_to_user(meme.stealer)
    message: str = "\nPosted by: {}\nTime: {}\nRating: {}\n\n".format(
        str(user.username), meme.post_time, sum_ratings(meme.id)
    )
    message += "```Tag / Vote{}User{}Platform{}Time UTC\n\n".format(" " * 10, " " * 16, " " * 12)
    message += "__initial post__{}{}{}{}{}{}".format(
        " " * 4,
        user.username,
        " " * (20 - len(user.username)),
        resolve_platform[user.platform],
        " " * (20 - len(resolve_platform[user.platform])),
        meme.post_time.strftime("%Y-%m-%d %H:%M:%S"),
    )

    tags: List[Tuple[Tags, Association, User]] = (
        database_handler.session.query(Tags, Association, User)
        .filter(
            Association.meme_id == int(meme_id), Association.tag_id == Tags.id, Association.added_by == User.user_id
        )
        .all()
    )
    ratig: List[Tuple[Ratings, User]] = (
        database_handler.session.query(Ratings, User)
        .filter(int(meme_id) == Ratings.meme_id, Ratings.added_by == User.user_id)
        .all()
    )

    time_line: List[Union[Tuple[int, Ratings, User], Tuple[Tags, Association, User]]] = sort_by_data(tags, ratig)
    message += merge_time_line(time_line)
    return message


def merge_time_line(time_line: List[Union[Tuple[int, Ratings, User], Tuple[Tags, Association, User]]]) -> str:
    message: str = ""
    for x in time_line:
        username: str = x[2].username
        if x[0] == 0:
            rate: int = x[1].rate
            message += "{}{}{}{}{}{}{}\n".format(
                rate_to_text(rate),
                " " * (20 - len(rate_to_text(rate))),
                username,
                " " * (20 - len(username)),
                resolve_platform[x[2].platform],
                " " * (20 - len(resolve_platform[x[2].platform])),
                x[1].time_added.strftime("%Y-%m-%d %H:%M:%S"),
            )
        elif type(x[0]) is Tags:
            if x[0].tag != "":
                tag: str = x[0].tag
                message += "{}{}{}{}{}{}{} UTC\n".format(
                    tag,
                    " " * (20 - len(tag)),
                    username,
                    " " * (20 - len(username)),
                    resolve_platform[x[2].platform],
                    " " * (20 - len(resolve_platform[x[2].platform])),
                    x[1].time_added.strftime("%Y-%m-%d %H:%M:%S"),
                )

    return "\n{}\n```".format(message)


def rate_to_text(vote: int) -> str:
    if vote == 1:
        return emoji.emojize(":arrow_up:")
    elif vote == -1:
        return emoji.emojize(":arrow_down:")
    else:
        raise ValueError


def sort_by_data(
    tags: List[Tuple[Tags, Association, User]], rating: List[Tuple[Ratings, User]]
) -> List[Union[Tuple[int, Ratings, User], Tuple[Tags, Association, User]]]:
    data: List[Union[Tuple[int, Ratings, User], Tuple[Tags, Association, User]]] = []
    for rat, use in rating:
        data.append((0, rat, use))
    data += tags
    data.sort(key=lambda date: datetime.strptime(str(date[1].time_added), "%Y-%m-%d %H:%M:%S"))
    return data


def rate_meme(meme_id: int, rate: int, user: str, platform: int) -> None:
    author_uuid: int = check_auther_registerd(user, platform)

    rating: Ratings = database_handler.session.query(Ratings).filter(
        Ratings.added_by == author_uuid, Ratings.meme_id == meme_id
    ).first()
    if not rating:
        Ratings.create(author_uuid, meme_id, rate)


def sum_ratings(meme_id: int) -> int:
    sum_rat: int = 0
    for x in database_handler.session.query(Ratings).filter(Ratings.meme_id == meme_id).all():
        sum_rat += x.rate
    return sum_rat


def id_to_user(user_id: int) -> "User":
    return database_handler.session.query(User).filter(User.user_id == user_id).first()


def id_to_meme(meme_id: int) -> str:
    meme = database_handler.session.query(Memes).filter(Memes.id == meme_id).first()
    if meme is None:
        return "There is no meme with this id"
    else:
        return prep4post(meme)
