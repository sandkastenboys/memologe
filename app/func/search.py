import random

from db_models import Memes, Tags, Association
from func.essentials import prep4post
from objects import session
from typing import List, Iterator


def strict_search(tags: list, amount: int):
    pass
    # mem: Association = session.query(Association).filter_by(Association.tag_id in tags).all()
    # for x in range(amount):


def soft_search(tags: list, amount: int):
    query_tags: List[str] = []
    for x in tags:
        query_tags.append(x.id)

    mem: list = session.query(Memes).filter(Association.tag_id.in_(query_tags),  # type: ignore
                                            Association.meme_id == Memes.id).all()
    if len(mem) == 0:
        return "Search query did not return any results."
    send_memes: list = []
    random.shuffle(mem)
    count: int = 0
    while amount > 0 and count < len(mem):
        if mem[count].id not in send_memes:
            send_memes.append(mem[count].id)
            yield prep4post(mem[count])
        count += 1


def yield_search(tags: str, count: int = 1) -> Iterator[str]:
    tag_list: list = tags.split(";")

    # eqivalent to WHERE id IN (..., ..., ...) Tag list
    tags: list = session.query(Tags).filter(Tags.tag.in_(tag_list)).all()  # type: ignore

    for _ in range(count):
        print("Soft search: tags {}".format(tags))
        print("Soft search: count {}".format(count))
        for meme in soft_search(tag_list, count):
            yield str(meme)
