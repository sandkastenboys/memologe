# pylint: disable=unused-variable

from typing import Union

from discord.ext import commands
from discord.ext.commands.context import Context

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
from func.static import show_help, translate
from objects import database_handler, logger


class DiscordAPI(commands.bot.Bot):
    def __init__(self):  # noqa: MC0001
        super().__init__(command_prefix=config["key"])
        self.remove_command("help")
        self.lang = translate()

        @self.event
        async def on_ready():
            logger.info("Reading Memes %s", config["read_on_start"])
            if config["read_on_start"] == "True":
                await self.read_meme_channel()

        @self.command(pass_context=True)
        async def help(ctx):
            await ctx.send(show_help())

        @self.command(pass_context=True)
        async def search(ctx, tags, count="1"):
            database_handler.check_mysql_connection()
            logger.info("Searching for %s of %s", count, tags)
            for msg in yield_search(tags, int(count)):
                await ctx.send(msg)

        @search.error
        async def search_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(self.lang["error"]["miss-arg-searcht"])
            else:
                logger.error(error, exc_info=True)
                raise error

        @self.command(name="random", pass_context=True)
        async def _random(ctx, count="1"):
            database_handler.check_mysql_connection()
            for msg in yield_random_meme(int(count)):
                post: Context = await ctx.send(msg)
                await post.add_reaction(chr(11014))
                await post.add_reaction(chr(11015))

        @self.command(pass_context=True)
        async def size(ctx):
            database_handler.check_mysql_connection()
            size: int = database_handler.session.query(Memes).count()
            await ctx.send(self.lang["info"]["db-meme-count"].format(size))

        @self.command(pass_context=True)
        async def post(ctx, link, tag):
            if "discord" in link:
                link: str = link.split("?")[0]
            if len(link) >= 512:
                await ctx.send(self.lang["error"]["link-to-long"])
                return
            database_handler.check_mysql_connection()
            add_meme(link, tag, ctx.message.author.name, 0, ctx.message.created_at)

        @post.error
        async def post_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(self.lang["error"]["miss-arg-link"])
            else:
                logger.error(error, exc_info=True)
                raise error

        @self.command(pass_context=True)
        async def category(ctx, id, tags):
            database_handler.check_mysql_connection()
            categorise_meme(id, tags, ctx.author.name, 0)
            await ctx.send(self.lang["success"]["tag-added"])

        @category.error
        async def category_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(self.lang["error"]["miss-arg-category"])
            else:
                logger.error(error, exc_info=True)
                raise error

        @self.command(pass_context=True)
        async def tags(ctx):
            database_handler.check_mysql_connection()
            tags: str = list_tags()
            if not tags.isspace():
                await ctx.send("```{}```".format(tags))
            else:
                await ctx.send(self.lang["info"]["db-no-tags"])

        @self.command(pass_context=True)
        async def posters(ctx):
            database_handler.check_mysql_connection()
            users: str = list_users()
            if users:
                await ctx.send(users)
            else:
                await ctx.send(self.lang["info"]["db-no-posters"])

        @self.command(pass_context=True)
        async def info(ctx, arg: str):
            if arg.isdigit():
                database_handler.check_mysql_connection()
                await ctx.send(history(int(arg)))
            else:
                await ctx.send(self.lang["error"]["miss-arg-info"])

        @info.error
        async def info_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(self.lang["error"]["miss-arg-info"])
            else:
                logger.error(error, exc_info=True)
                raise error

        @self.command(pass_context=True)
        async def idtomeme(ctx, arg):
            database_handler.check_mysql_connection()
            x = await ctx.send(id_to_meme(int(arg)))
            await x.add_reaction(chr(11014))
            await x.add_reaction(chr(11015))

        @idtomeme.error
        async def idtomeme_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(self.lang["error"]["miss-arg-idtomeme"])
            else:
                logger.error(error, exc_info=True)
                raise error

        @self.event
        async def on_reaction_add(reaction, user):
            if user != self.user:
                logger.debug("Username %s / User %s", user.name, user)
                database_handler.check_mysql_connection()
                msg = reaction.message
                meme_id: int = int(msg.content.split(" ")[4])

                if str(reaction) == chr(11014):
                    rate_meme(meme_id, 1, user.name, 0)
                elif str(reaction) == chr(11015):
                    rate_meme(meme_id, -1, user.name, 0)

                await msg.channel.send(self.lang["success"]["vote-added"].format(user.name))

    async def read_meme_channel(self) -> None:
        for channel in self.get_all_channels():
            if channel.name == "memes" or channel.name == "cursed-images":
                await self.process(channel)

    async def process(self, channel):
        logger.debug("Called from channel %s", channel)
        async for message in channel.history(limit=10000):
            link: Union[str, bool] = find_link(message.content)

            if type(link) is str:
                if "discord" in link:
                    link: str = link.split("?")[0]
                if len(link) < 512:
                    logger.info("Added meme with link %s", link)
                    add_meme(link, "", message.author.name, 0, message.created_at)
