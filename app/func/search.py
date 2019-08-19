import random
from typing import Iterator, List

from db_models import Association, Memes, Tags, Ratings
from func.essentials import prep4post
from objects import database_handler
from config import config


def strict_search(tags: list, amount: int):
    pass
    # mem: Association = session.query(Association).filter_by(Association.tag_id in tags).all()
    # for x in range(amount):


def soft_search(tags: list, amount: int):
    query_tags: List[str] = []
    for x in tags:
        query_tags.append(x.id)

    mem: list = database_handler.session.query(Memes).filter(
        Association.tag_id.in_(query_tags),  # type: ignore
        Association.meme_id == Memes.id,
    ).all()
    if len(mem) == 0:
        return "Search query did not return any results."
    send_memes: list = []
    random.shuffle(mem)
    for count in range(min(len(mem), amount, config["max_post"])):
        if mem[count].id not in send_memes:
            send_memes.append(mem[count].id)
            yield prep4post(mem[count])


def yield_search(tags: str, count: int = 1) -> Iterator[str]:
    tag_list: list = tags.split(";")

    # eqivalent to WHERE id IN (..., ..., ...) Tag list
    tags_list: list = database_handler.session.query(Tags).filter(
        Tags.tag.in_(tag_list)  # type: ignore
    ).all()

    for meme in soft_search(tags_list, count):
        yield str(meme)


class TopMemes:

    def __init__(self) -> 'TopMemes':

        self.top_memes = []

    def update_top_memes(self) -> None:
        temp_raiting : dict = {}
        all_likes: list = database_handler.session.query(Ratings).all()
        for rating in all_likes:
            if rating.meme_id in temp_raiting:
                temp_raiting[rating.meme_id] += rating.rate
            else:
                temp_raiting[rating.meme_id] = rating.rate
        sorted_d = sorted((key, value) for (key,value) in temp_raiting.items())
        self.top_memes = sorted_d[:10]

    def get_top_memes(self) -> Iterator:
        return_query: List[Memes] = database_handler.session.query(Memes).filter(Memes.id in self.top_memes).all()
        for meme in return_query:
            yield prep4post(meme)