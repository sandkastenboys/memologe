# pylint: disable=unused-variable

from discord.ext import commands
from discord.ext.commands.context import Context
from objects import session
from typing import Union

from config import config
from db_models import Memes
from func.essentials import (
    add_meme,
    categorise_meme,
    find_link,
    history,
    id_to_meme,
    list_tags,
    list_users,
    rate_meme,
    yield_random_meme,
)
from func.search import yield_search
from func.static import show_help


class DiscordAPI(commands.bot.Bot):
    def __init__(self):
        super().__init__(command_prefix=config["key"])
        self.remove_command("help")

        @self.event
        async def on_ready():
            print(config["read_on_start"])
            if config["read_on_start"] == "True":
                await self.read_meme_channel()

        @self.command(pass_context=True)
        async def help(ctx):
            await ctx.send(show_help())

        @self.command(pass_context=True)
        async def search(ctx, tags, count):
            print("Searching for {} of {}".format(count, tags))
            for msg in yield_search(tags, count):
                await ctx.send(msg)

        @search.error
        async def search_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("Empty query. You need to specify tags to search.")
            else:
                raise error

        @self.command(name="random", pass_context=True)
        async def _random(ctx, count="1"):
            for msg in yield_random_meme(int(count)):
                post: Context = await ctx.send(msg)
                await post.add_reaction(chr(11014))
                await post.add_reaction(chr(11015))

        @self.command(pass_context=True)
        async def size(ctx):
            size: int = session.query(Memes).count()
            await ctx.send("There are : {} memes in the database".format(size))

        @self.command(pass_context=True)
        async def post(ctx, link, tag):
            if "discord" in link:
                link: str = link.split("?")[0]
            if len(link) >= 512:
                await ctx.send("Link is to long. Max length is 512 characters.")
                return

            add_meme(link, tag, ctx.author.name, 0, ctx.created_at)

        @post.error
        async def post_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(
                    "You need to specify a link to a meme and tags you want to set."
                )
            else:
                raise error

        @self.command(pass_context=True)
        async def category(ctx, id, tags):
            categorise_meme(id, tags, ctx.author.name, 0)
            await ctx.send("Tag has been added.")

        @category.error
        async def category_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(
                    "You need to specify an id of a meme and tags you want to set."
                )
            else:
                raise error

        @self.command(pass_context=True)
        async def tags(ctx):
            tags: str = list_tags()
            if not tags.isspace():
                await ctx.send("```{}```".format(tags))
            else:
                await ctx.send("There are no tags in the database.")

        @self.command(pass_context=True)
        async def posters(ctx):
            users: str = list_users()
            if users:
                await ctx.send("```{}```".format(users))
            else:
                await ctx.send("There are no posters in the database.")

        @self.command(pass_context=True)
        async def info(ctx, arg):
            await ctx.send(history(arg))

        @info.error
        async def info_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(
                    "You need to specify the id of the meme you want more info about."
                )
            else:
                raise error

        @self.command(pass_context=True)
        async def idtomeme(ctx, arg):
            x = await ctx.send(id_to_meme(int(arg)))
            await x.add_reaction(chr(11014))
            await x.add_reaction(chr(11015))

        @idtomeme.error
        async def idtomeme_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(
                    "You need to specify the id of the meme you want to show."
                )
            else:
                raise error

        @self.event
        async def on_reaction_add(reaction, user):
            if user != self.user:
                print(user.name, "/", user)

                msg = reaction.message
                print(msg.content.split(" ")[8])
                meme_id: int = int(msg.content.split(" ")[8])

                if str(reaction) == chr(11014):
                    rate_meme(meme_id, 1, user.name, 0)
                elif str(reaction) == chr(11015):
                    rate_meme(meme_id, -1, user.name, 0)

                await msg.channel.send("Thx for your rating, {}".format(user.name))

    async def read_meme_channel(self):
        for channel in self.get_all_channels():
            if channel.name == "memes" or channel.name == "cursed-images":
                await self.process(channel)

    async def process(self, channel):
        print("call:", channel)
        async for message in channel.history(limit=10000):
            link: Union[str, bool] = find_link(message.content)

            if type(link) is str:
                if "discord" in link:
                    link: str = link.split("?")[0]
                if len(link) >= 512:
                    continue

                print(link)
                add_meme(link, "", message.author.name, 0, message.created_at)
