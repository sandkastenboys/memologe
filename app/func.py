from MySql_DB import Memes, Tags
from objects import session
from uuid import uuid4
from config import config
from sqlalchemy import func, select
import requests
import shutil

def random_meme():
    meme : Memes = session.query(Memes).order_by(func.random()).first()

    if meme is None:

        return "There are 0 memes in the database"

    return meme

def download(link : str):
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

def check_existens(link : str) -> bool:
    device  = session.query(Memes).filter_by(link = link).first()

    return device is not None


def check_for_link(link):
    return "http" in link.content


def find_link(post: str):
    try:
        ind = post.index("http")
        temp = post[ind:].split(" ")
        return temp[0]
    except:
        return False
