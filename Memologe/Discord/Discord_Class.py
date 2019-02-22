import discord
import discord.server
import asyncio
import emoji
import argparse
from config import config
from Memologe.MySql_DB import db
import time
import random

last_time = 0

def check_for_link(link):
    return "http" in link.content


def find_link(post: str):
    try:
        ind = post.index("http")
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

                try:
                    how_many = int(message.content.split(" ")[1])
                    if how_many > 10:
                        how_many = 10
                except:
                    how_many = 1

                for x in range(how_many):
                    ran_id = random.randint(0, db.max_id())

                    meme = db.get_meme_by_id(ran_id)

                    await self.send_message(message.channel, 'Here your meme: ' + meme[1])


            if message.content.startswith(config["key"] + 'cate_meme'):
                command = message.content.split(" ")[1:]

                tags = ""

                if db.check_ex(command[0]) is True:
                    id_s = db.get_meme_id_by_link(command[0])
                    if command[1][-1] != ";":
                        command[1] += ";"

                    if id_s[0][2] == "":
                        tags = command[1]

                    elif id_s[0][2][-1] != ";":
                        tags = id_s[0][2] + ";" + command[1]

                    db.add_tags_by_id(id_s[0][0], tags)

            if message.content.startswith(config["key"] + 'help'):
                await self.send_message(message.channel, 'Memologe Commands:')
                await self.send_message(message.channel, ':arrow_right: $post_meme <link> <tags> seperate multiple tags with ;')
                await self.send_message(message.channel, ':arrow_right: $ran_meme <how_many> posts random meme')
                await self.send_message(message.channel, ':arrow_right: $search <tag> <how_many = 1> searches memes based on tag')
                await self.send_message(message.channel, ':arrow_right: $size amount of memes in the db')

            if message.content.startswith(config["key"] + "post_meme"):

                meme = message.content.split(" ")[1:]
                print(db.check_ex(meme[0]))
                if db.check_ex(meme[0]) is False and type(find_link(meme[0])) is str:
                    try:
                        if meme[1][-1] != ";":
                            meme[1] += ";"
                    except:
                        meme.append("")
                    db.add_meme(meme[0], int(time.time()), meme[1])
                    await self.post_meme(meme[0])
                    db.add_tags(meme[1])
                else:
                    await self.send_message(message.channel, "This Meme already got posted")

            if message.content.startswith(config["key"] + "size"):
                size = db.size_of_db()

                await self.send_message(message.channel, "There are : " + str(size[0][0]) + " memes in the database")

            if message.content.startswith(config["key"] + "search"):
                tag = message.content.split(" ")[1]
                try:
                    how_many = int(message.content.split(" ")[2])
                except:
                    how_many = 1

                data = db.search_meme(tag)
                random.shuffle(data)

                count = 0
                while count < how_many:
                    if tag + ";" in data[count][2] or data[count][2].split(";")[-1] == tag:
                        await self.send_message(message.channel, data[count][1])
                    count += 1
                    if count >= len(data):
                        break

            if message.content.startswith(config["key"] + "tags"):
                await self.send_message(message.channel, "```" + "\n".join(db.tags) + "```")

            if message.content.startswith(config["key"] + "recent"):
                data = db.get_recent(10000,10)
                for x in data:
                    await self.send_message(message.channel, x[1])

        @self.event
        async def on_reaction_add(reaction, user):
            if str(user) != "Memologe#3481":
                # channel = reaction.message.channel

                await self.clear_reactions(reaction.message)
                await self.add_reaction(reaction.message, chr(11014))
                await self.add_reaction(reaction.message, chr(11015))

            # await self.send_message(user, "Thx for your rating")

    async def post_meme(self, link: str):
        for server in self.servers:
            for channel in server.channels:
                if channel.name == 'memes_lib':
                    await self.send_message(channel, link)

    async def read_meme_channel(self): # This Funktion just reads the entire meme channel (not used anylonger)
        for server in self.servers:
            for channel in server.channels:
                if channel.name == 'memes':
                    async for message in self.logs_from(channel, limit=10000):
                        link = find_link(message.content)
                        if type(link) is str:
                            if db.check_ex(link) is False:
                                print("add meme:", link)
                                db.add_meme(link, int(time.time()), "")
                                await self.post_meme(link)



d = Discord_API()
d.run(config["token"])
