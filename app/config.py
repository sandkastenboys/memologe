import os
from typing import Union, Tuple, List

to_load: List[Union[Union[Tuple[str, int], Tuple[str, str], any]]] = [

    ("debug", "False"),

    # sqlalchemy
    ("MYSQL_HOSTNAME", "127.0.0.1"),
    ("MYSQL_PORT", 3306),
    ("MYSQL_DATABASE", "memes"),
    ("MYSQL_USERNAME", "travis"),
    ("MYSQL_PASSWORD", ""),

    # core functionality
    ("max_post", 10),
    ("save", "True"),
    ("destination", "/mnt/hdd/memes/"),
    ("read_on_start", "False"),

    # discord
    ("botname", ""),
    ("key", "$"),

    # tokens
    ("tele_token", ""),  # Telegram Bot token
    ("disc_token", ""),  # Discord Bot Token

]

# the final configuration dict
config: dict = {}

# load all configuration values from the env
for key in to_load:
    if isinstance(key, tuple):
        if key[0] in os.environ:
            config[key[0]] = os.environ.get(key[0])
        else:
            config[key[0]] = key[1]
    elif key in os.environ:
        config[key] = os.environ.get(key)

# set sqlalchemy database connection uri
config["SQLALCHEMY_DATABASE_URI"]:
    str = f"mysql+pymysql://{config['MYSQL_USERNAME']}:{config['MYSQL_PASSWORD']}@" \
        f"{config['MYSQL_HOSTNAME']}:{config['MYSQL_PORT']}/{config['MYSQL_DATABASE']}"
