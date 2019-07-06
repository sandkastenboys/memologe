import random

from db_models import Memes, Tags, Association
from func.essentials import parse_amount, prep4post
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

    mem: list = session.query(Memes).filter(Association.tag_id.in_(query_tags), Association.meme_id == Memes.id).all()
    send_memes: list = []
    random.shuffle(mem)
    count: int = 0
    while amount > 0 and count < len(mem):
        if mem[count].id not in send_memes:
            send_memes.append(mem[count].id)
            yield prep4post(mem[count])
        count += 1


def yield_search(message: list) -> Iterator[str]:  # $search tag1;tag2;tag3 10 1 -> Tags Amount Only
    possible_tags: list = message[0].split(";")
    # eqivalent to WHERE id IN (..., ..., ...) Tag list
    tags: list = session.query(Tags).filter(Tags.tag.in_(possible_tags)).all()
    try:
        amount: int = parse_amount(message[1])
    except IndexError:
        amount = 1
    try:
        only_this_tags = message[2]
    except IndexError:
        only_this_tags = "True"

    for _ in range(amount):
        if only_this_tags == "False":
            yield "Strict Search not implemented yet"
            break
            # for meme in strict_search(tags, amount):
            #   yield str(meme)
        else:
            for meme in soft_search(tags, amount):
                yield str(meme)
