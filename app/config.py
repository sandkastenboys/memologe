import os
from typing import Dict, List, Tuple, Union

to_load: List[Union[Union[Tuple[str, Union[int, str]]]]] = [
    # sqlalchemy
    ("sqlite", "False"),
    ("MYSQL_HOSTNAME", "127.0.0.1"),
    ("MYSQL_PORT", 3306),
    ("MYSQL_DATABASE", "memes"),
    ("MYSQL_USERNAME", "travis"),
    ("MYSQL_PASSWORD", ""),
    # core functionality
    ("max_post", 10),
    ("save_memes_to_disc", "True"),
    ("destination", "/app/app/data/"),
    ("config_log_destination", "/app/app/log/"),
    ("read_on_start", "False"),
    # discord
    ("key", "$"),
    # tokens
    ("telegram_token", ""),
    ("discord_token", ""),
]

# the final configuration dict
config: Dict[str, Union[str, int, None]] = {}

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
config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{config['MYSQL_USERNAME']}:{config['MYSQL_PASSWORD']}@"
    f"{config['MYSQL_HOSTNAME']}:{config['MYSQL_PORT']}/{config['MYSQL_DATABASE']}"
)
