from typing import Dict


resolve_platform: Dict[int, str] = {
    0 : "Discord",
    1 : "Telegram"
}


def help() -> str:

    return "Memologe Help ```"\
        "- $post_meme <link> <tags>         seperate multiple tags with ';'\n"\
        "- $ran_meme <how_many = 1>         posts random meme\n"\
        "- $cate_meme <id> <tags>           adds these tags to the meme so that it can be found more easily\n"\
        "- $search <tag> <how_many = 1>     searches memes based on tag\n"\
        "- $size                            amount of memes in the db\n"\
        "- $info <id>                       returns relevant information about the meme with this id\n"\
        "- $posters                         returns list of most active users of this bot\n"\
        "- $tags                            returns all tags in the database\n"\
        "- $id2meme                         returns meme with this id\n\n"\
        "Example Meme Post:\n$post_meme https://cdn.discordapp.com/attachments/344431213550764034/589167907070804009/64587415_744264206054251_7518656262456737792_n.png school;kid;skyrim;100\n\n"\
        "Example Categorise Meme:\n"\
        "$cate_meme 23 minecraft;engineer\n\n"\
        "``` When you have further Questions or Bug Reports see contacts: https://spartanerspaten.github.io/"
