import os
from typing import Union, Tuple, List

to_load: List[Union[Union[Tuple[str, int], Tuple[str, str], Tuple[str, bool], any]]] = [

    # sqlalchemy
    ("MYSQL_HOSTNAME", "db"),
    ("MYSQL_PORT", 3307),
    ("MYSQL_DATABASE", "memes"),
    ("MYSQL_USERNAME", "memologe"),
    ("MYSQL_PASSWORD", "memes_are_the_best"),  # TODO CHANGE!

    ("tele_token", "778745612:AAHFnKvwmRTvS2wDtBlAvbCHXmHgjum9hYM"),  # Telegram Bot token
(   "botname", "Memologe#3481"),
    ("max_post", 10),
    ("disc_token", "NTM2NjIxMzc2NjQ4MzgwNDQ1.DyetMw.blkw2eKf4LF_XlUmIgIf2Led470"),  # Discord Bot Token
    ("key", "$"),
    ("save", True),
    ("destination", "/home/einspaten/hdd/memes/"),
    ("read_on_start", "False"),
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
config["SQLALCHEMY_DATABASE_URI"]: str = \
    f"mysql+pymysql://{config['MYSQL_USERNAME']}:{config['MYSQL_PASSWORD']}@" \
        f"{config['MYSQL_HOSTNAME']}:{config['MYSQL_PORT']}/{config['MYSQL_DATABASE']}"
