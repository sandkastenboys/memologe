import os
from configparser import ConfigParser
from typing import Dict

resolve_platform: Dict[int, str] = {0: "Discord", 1: "Telegram"}


def show_help() -> str:
    return (
        "Memologe Help ```"
        "- $post <link> <tags>              seperate multiple tags with ';'\n"
        "- $random <count = 1>              posts random meme\n"
        "- $category <id> <tags>            adds these tags to the meme so that it can be found more easily\n"
        "- $search <tag> <count = 1>        searches memes based on tag\n"
        "- $size                            amount of memes in the db\n"
        "- $info <id>                       returns relevant information about the meme with this id\n"
        "- $posters                         returns list of most active users\n"
        "- $tags                            returns all tags in the database\n"
        "- $idtomeme <id>                   returns the meme with this id\n\n"
        "Example meme post:\n$post_meme  https://cdn.discordapp.com/attachments/344431213550764034/"
        "589167907070804009/64587415_744264206054251_7518656262456737792_n.png school;kid;skyrim;100\n\n"
        "Example categorise meme:\n"
        "$cate_meme 23 minecraft;engineer\n\n"
        "```\n"
        "When you have further questions, see contacts here: https://spartanerspaten.github.io/ \n"
        "Please reports bugs here: https://github.com/SpartanerSpaten/Memologe/"
    )


def translate(language: str = "en", path: str = "app/translate") -> ConfigParser:
    translate: ConfigParser = ConfigParser()
    lang_file = "{}/{}.ini".format(path, language)
    if os.path.isfile(lang_file):
        translate.read(lang_file)
    else:
        print(os.getcwd())
        raise FileNotFoundError
    print("Translate sections {}".format(translate.sections()))
    print(
        "Translate keys {}".format(
            {section: dict(translate[section]) for section in translate.sections()}
        )
    )
    return translate
