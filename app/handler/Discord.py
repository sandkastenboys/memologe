# pylint: disable=unused-variable

from func.static import help
from objects import session
import discord
from config import config
from db_models import Memes
from func.search import yield_search
from func.essentials import (post_meme, find_link, yield_random_meme, categorise_meme,
                             list_tags, list_users, history, rate_meme, id2meme)

last_time = 0


class DiscordAPI(discord.Client):
    def __init__(self):
        super().__init__()

        @self.event
        async def on_ready():
            print(config["read_on_start"])
            if config["read_on_start"] == 'True':
                await self.read_meme_channel()

        @self.event
        async def on_message(message):
            if message.content.startswith(config["key"] + 'ran_meme'):
                for ms in yield_random_meme(message.content):
                    x = await message.channel.send(ms)
                    await x.add_reaction(chr(11014))
                    await x.add_reaction(chr(11015))

            if message.content.startswith(config["key"] + 'help'):
                await message.channel.send(help())

            if message.content.startswith(config["key"] + "search"):

                for ms in yield_search(message.content.split(" ")[1:]):
                    x = await message.channel.send(ms)

            if message.content.startswith(config["key"] + "size"):
                size: int = session.query(Memes).count()

                await message.channel.send("There are : " + str(size) + " memes in the database")

            if message.content.startswith(config["key"] + "post_meme"):
                link: str = message.content.split(" ")[1]
                if 'discord' in link:
                    link: str = link.split("?")[0]
                if len(link) >= 512:
                    await message.channel.send("Link is to long. Max length is 512 characters.")
                    return

                post_meme(link, message.content.split(" ")[2], message.author.name, 0,
                          message.created_at)

            if message.content.startswith(config["key"] + "cate_meme"):
                args: list = message.content.split(" ")[1:]

                categorise_meme(args[0], args[1], message.author.name, 0)

            if message.content.startswith(config["key"] + "tags"):
                await message.channel.send("```" + list_tags() + "```")

            if message.content.startswith(config["key"] + "posters"):
                await message.channel.send("```" + list_users() + "```")

            if message.content.startswith(config["key"] + "info"):
                await message.channel.send(history(message.content.split(" ")[1]))

            if message.content.startswith(config["key"] + "id2meme"):
                x = await message.channel.send(id2meme(int(message.content.split(" ")[1])))
                await x.add_reaction(chr(11014))
                await x.add_reaction(chr(11015))

        @self.event
        async def on_reaction_add(reaction, user):

            if str(user) != config["botname"]:
                print(user.name, "/", user)
                meme_id: int = int(reaction.message.content.split(" ")[8])

                if str(reaction) == chr(11014):
                    rate_meme(meme_id, 1, user.name, 0)
                elif str(reaction) == chr(11015):
                    rate_meme(meme_id, -1, user.name, 0)

            # await self.send_message(user, "Thx for your rating")

    async def post_meme(self, link: str):
        for channel in self.get_all_channels():
            if channel.name == 'memes_lib':
                await channel.send(link)

    async def read_meme_channel(self):

        for channel in self.get_all_channels():
            if channel.name == 'memes' or channel.name == "cursed-images":
                await self.process(channel)

    async def process(self, channel):
        print("call:", channel)
        async for message in channel.history(limit=10000):
            link: Union[str, bool] = find_link(message.content)

            if type(link) is str:
                if 'discord' in link:
                    link: str = link.split("?")[0]
                if len(link) >= 512:
                    continue

                print(link)
                post_meme(link, "", message.author.name, 0, message.created_at)
