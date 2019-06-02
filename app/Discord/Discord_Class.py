import argparse
import discord
from config import config
from MySql_DB import Memes, Tags
import time
import random
from func import random_meme, check_existens, find_link,download
from objects import *

last_time = 0

class Discord_API(discord.Client):
    def __init__(self):
        super().__init__()

        @self.event
        async def on_ready():
            pass
            await self.read_meme_channel()

        @self.event
        async def on_message(message):
            if message.content.startswith(config["key"] + 'ran_meme'):

                try:
                    how_many = int(message.content.split(" ")[1])
                    if how_many > 10:
                        how_many = 10
                except:
                    how_many = 1

                for x in range(how_many):
                    meme = random_meme()

                    await message.channel.send('Here your meme: ' + meme.link)


            if message.content.startswith(config["key"] + 'help'):


                await message.channel.send('Memologe Commands:')
                await message.channel.send(':arrow_right: $post_meme <link> <tags> seperate multiple tags with ;')
                await message.channel.send(':arrow_right: $ran_meme <how_many> posts random meme')
                await message.channel.send(':arrow_right: $search <tag> <how_many = 1> searches memes based on tag')
                await message.channel.send(':arrow_right: $size amount of memes in the db')

            if message.content.startswith(config["key"] + "search"):

                tags = session.query(Tags).filter_by(tag = message.content.split(" ")[1]).all()

                meme = message.content.split(" ")[2]

                if meme == "": how_many = 1
                else:
                    try:
                        how_many = int(meme)
                    except:
                        how_many = 1

                for x in range(how_many):

                    tag = random.choice(tags)

                    meme = session.query(Memes).filter_by(uuid = tag)

                    await message.channel.send(meme.link)


            if message.content.startswith(config["key"] + "size"):
                size = session.query(Memes).count()

                await message.channel.send("There are : " + str(size) + " memes in the database")

            if message.content.startswith(config["key"] + "post_meme"):

                meme = message.content.split(" ")[1:]
                if not check_existens(meme[0]) and type(find_link(meme[0])) is str:

                    if config["download"] is True:
                        filename = download(meme[0])
                    else:
                        filename = ""


                    cm : Memes = Memes.create(meme[0], filename, message.auther.name)

                    if meme[1] != "":

                        tags : list = meme[1].split(";")

                        for tag in tags:

                            Tags.create(cm.uuid, tag)

                    await self.post_meme(meme[0])

                else:

                    await message.channel.send("This Meme already got posted")


        @self.event
        async def on_reaction_add(reaction, user):
            if str(user) != "Memologe#3481":
                # channel = reaction.message.channel

                await reaction.message.clear_reactions()
                await reaction.message.add_reaction(chr(11014))
                await reaction.message.add_reaction(chr(11015))

            # await self.send_message(user, "Thx for your rating")

    async def post_meme(self, link: str):
        for channel in self.get_all_channels():
            if channel.name == 'memes_lib':
                await channel.send(link)

    async def read_meme_channel(self): # This Funktion just reads the entire meme channel (not used anylonger)

        for channel in self.get_all_channels():
            if channel.name == 'memes' or channel.name == "cursed-images":
                await self.prozess(channel)


    async def prozess(self, channel):
        print("call:", channel)
        async for message in channel.history():
            link = find_link(message.content)
            if type(link) is str:
                if check_existens(link) is False:
                    print("added to database:", link)
                    if config["save"] is True:
                        filename = download(link)
                    else:
                        filename = ""
                    Memes.create(link, filename, message.author.name)

                   # await self.post_meme(link)
