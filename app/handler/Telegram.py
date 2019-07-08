from typing import Callable, List, Tuple, Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.bot import Bot
from telegram.callbackquery import CallbackQuery
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater
from telegram.ext.dispatcher import run_async
from telegram.message import Message
from telegram.update import Update

from config import config
from db_models import Memes
from func.essentials import (
    add_meme,
    categorise_meme,
    history,
    id_to_meme,
    list_tags,
    list_users,
    rate_meme,
    yield_random_meme,
)
from func.search import yield_search
from func.static import show_help
from objects import session

keyboard = [
    [InlineKeyboardButton("UpVote", callback_data="UpVote")],
    [InlineKeyboardButton("DownVote", callback_data="DownVote")],
]
keyboard_markup = InlineKeyboardMarkup(keyboard)


def parse_count(args: List[str], position: int, default: int = 1) -> Tuple[int, str]:
    if len(args) < position + 1:
        count: int = default
    elif len(args) >= position and args[position].isdigit():
        count: int = abs(int(args[0]))
    else:
        return (0, str(position) + " argument should be an positive integer")
    return (count, "")


@run_async
def post_meme(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message

    if len(args) == 0:
        message.reply_text("You have to at least give a link")
        return

    link: str = args[0]

    if len(args) == 1:
        post_tags: str = ""
    else:
        post_tags: str = args[1]

    message.reply_text(
        add_meme(link, post_tags, message.from_user.username, 1, message.date)
    )


@run_async
def random(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message

    number: Tuple[int, str] = parse_count(args, 0)
    if number[1]:
        message.reply_text(number[1])
        return

    count: int = number[0]

    for msg in yield_random_meme(count):
        message.reply_text(msg, reply_markup=keyboard_markup)


@run_async
def userhelp(bot: Bot, update: Update, args: List[str]) -> None:
    update.message.reply_text(show_help(), parse_mode="Markdown")


@run_async
def _size(bot: Bot, update: Update, args: List[str]) -> None:

    size: int = session.query(Memes).count()
    update.message.reply_text(
        "There are : {} memes in the database".format(size), parse_mode="Markdown"
    )


@run_async
def search(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message
    if len(args) < 2:
        count: int = 1
    elif args[1].isdigit():
        if int(args[1]) < 0:
            message.reply_text("Your given number is below 0")
            return
        else:
            count: int = int(args[1])
    else:
        count: int = 1
    tags = args[0]

    print("Searching for {} of {}".format(count, tags))
    for msg in yield_search(tags, count):
        message.reply_text(msg, reply_markup=keyboard_markup)


@run_async
def _tags(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message
    tags: str = list_tags()
    if tags.isspace():
        message.reply_text("There are no tags in the database.")
    else:
        message.reply_text("```{}```".format(tags), parse_mode="Markdown")


@run_async
def posters(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message
    users: str = list_users()
    if users:
        message.reply_text("```{}```".format(users), parse_mode="Markdown")
    else:
        message.reply_text("There are no posters in the database.")


@run_async
def idtomeme(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message

    if len(args) == 0:
        message.reply_text("You have to give an id")
        return
    elif args[0].isdigit():
        message.reply_text("You have to give an integer")
        return

    count: int = int(args[0])
    message.reply_text(id_to_meme(count), reply_markup=keyboard_markup)


@run_async
def category(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message
    if len(args) < 2:
        message.reply_text(
            "You have to specify your meme_id and the tags you want to add ... not enough arguemts"
        )
        return
    if args[0].isdigit():
        if int(args[1]) < 0:
            message.reply_text("Your given number is below 0")
            return
        else:
            meme_id: int = int(args[1])
        tags: str = args[1]
    else:
        message.reply_text("meme_id has to be an integer")
        return
    categorise_meme(meme_id, tags, message.from_user.username, 1)
    message.reply_text("thx for your help")


@run_async
def _info(bot: Bot, update: Update, args: List[str]) -> None:
    message: Message = update.message
    if len(args) == 0:
        message.reply_text(
            "You have to specify your meme_id and the tags you want to add ... not enough arguemts"
        )
        return
    if args[0].isdigit():
        meme_id: int = int(args[0])
    else:
        message.reply_text("meme_id has to be an integer")
        return
    text: str = history(meme_id)
    message.reply_text(text, parse_mode="Markdown")


@run_async
def upvote(bot: Bot, update: Update) -> None:
    query: CallbackQuery = update.callback_query
    username: str = query.from_user.username
    meme_id: int = int(query.message.text.split(" ")[8])
    rate_meme(meme_id, 1, username, 1)


@run_async
def downvote(bot: Bot, update: Update) -> None:
    query: CallbackQuery = update.callback_query
    username: str = query.from_user.username
    meme_id: int = int(query.message.text.split(" ")[8])
    rate_meme(meme_id, -1, username, 1)


def init_telegram():

    updater: Updater = Updater(config["telegram_token"])

    commands: List[List[Union[str, Callable]]] = [
        ["post", post_meme],
        ["random", random],
        ["help", userhelp],
        ["size", _size],
        ["search", search],
        ["tags", _tags],
        ["posters", posters],
        ["idtomeme", idtomeme],
        ["category", category],
        ["info", _info],
    ]

    for command, function in commands:
        updater.dispatcher.add_handler(
            CommandHandler(command, function, pass_args=True)
        )

    updater.dispatcher.add_handler(CallbackQueryHandler(upvote, pattern="UpVote"))
    updater.dispatcher.add_handler(CallbackQueryHandler(downvote, pattern="DownVote"))
    updater.start_polling()
