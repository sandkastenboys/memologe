import discord
import discord.server
import asyncio
import emoji
import argparse
from config import config
from Memologe.MySql_DB import DB
import time
import random

last_time : int = 0


def check_for_link(link):
    return "http" in link.content

def find_link(post:str):
    try:
        ind : int = post.index("http")
        temp = post[ind:].split(" ")
        return temp[0]
    except:
        return False

class Discord_API(discord.Client):
    def __init__(self):
        super().__init__()

        @self.event
        async def on_message(message):
            if message.content.startswith(config["key"] + 'ran_meme'):

                ran_id : int = random.randint(0,db.max_id())

                meme = db.get_meme_by_id(ran_id)

                await self.send_message(message.channel, 'Here your meme: ' + meme[1])

                #await self.edit_message(tmp, 'You have {} messages :joy:')

            if message.content.startswith(config["key"] + 'cate_meme'):
                command = message.content.split(" ")[1:]
                server = list(self.servers)[0]
                print(message.user)
                print(server)

            if message.content.startswith( config["key"] + 'help'):
                await self.send_message(message.channel, 'Memologe Commands:')
                await self.send_message(message.channel, ':arrow_right: ```$post_meme <link> <tags>``` seperate multiple tags with ;')
                await self.send_message(message.channel, ':arrow_right: ```$ran_meme``` posts random meme')


            if message.content.startswith( config["key"] + "post_meme"):

                meme: list = message.content.split(" ")[1:]
                print(db.check_ex(meme[0]))
                if db.check_ex(meme[0]) is False:
                    print("ADD:",meme)
                    db.add_meme(meme[0],int(time.time()),meme[1])
                    await self.post_meme(meme[0])
                else:
                    await self.send_message(message.channel, "This Meme already got posted")

                #if time.time() - last_time > 86400:
                #    await self.read_meme_channel()

            if message.content.startswith(config["key"] + "size"):

                size = db.size_of_db()

                await self.send_message(message.channel, "There are : " + str(size[0][0]) + " memes in the database")



        @self.event
        async def on_reaction_add(reaction, user):
            print(type(user),user)
            if str(user) != "Memologe#3481":

                #channel = reaction.message.channel

                await self.clear_reactions(reaction.message)
                await self.add_reaction(reaction.message, chr(11014))
                await self.add_reaction(reaction.message, chr(11015))

               # await self.send_message(user, "Thx for your rating")
    async def post_meme(self, link:str):
        for server in self.servers:
            for channel in server.channels:
                if channel.name == 'memes_lib':
                    await self.send_message(channel, link)

    async def read_meme_channel(self):
        for server in self.servers:
            for channel in server.channels:
                if channel.name == 'memes':
                    async for message in self.logs_from(channel, limit=10000):
                        link = find_link(message.content)
                        if type(link) is str:
                            if db.check_ex(link) is False:
                                print("add meme:", link)
                                db.add_meme(link,int(time.time()),"")
                                await self.post_meme(link)


            #db.add_meme(meme[0], time.time(), meme[1])
db = DB()
d = Discord_API()
d.run(config["token"])