import telepot
from config import config
from telepot.loop import MessageLoop
from db_models import Memes
import random
from func.essentials import yield_random_meme, list_tags, list_users, rate_meme, history
from func.search import yield_search
from func.static import help
from objects import session
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='UpVote', callback_data='UpVote'),
     InlineKeyboardButton(text='DownVote', callback_data='DownVote')],
])


# https://telepot.readthedocs.io/en/latest/
def handle(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    message = message.get("text")

    if chat_type == "supergroup":
        message = list(message)
        message[0] = config["key"]
        message = "".join(message)

    if message.startswith(config["key"] + 'ran_meme'):

        for ms in yield_random_meme(message):
            print(ms)
            bot.sendMessage(chat_id, ms, reply_markup=keyboard)

    if message.startswith(config["key"] + 'help'):
        bot.sendMessage(chat_id, help(), parse_mode='Markdown')

    if message.startswith(config["key"] + 'size'):
        size: int = session.query(Memes).count()

        bot.sendMessage(chat_id, "There are : " + str(size) + " memes in the database")

    if message.startswith(config["key"] + 'search'):
        for ms in yield_search(message.split(" ")[1:]):
            bot.sendMessage(chat_id, ms, reply_markup=keyboard)

    if message.startswith(config["key"] + 'tags'):
        bot.sendMessage(chat_id, "```" + list_tags() + "```", parse_mode='Markdown')

    if message.startswith(config["key"] + "posters"):
        bot.sendMessage(chat_id, "```" + list_users() + "```", parse_mode='Markdown')

    if message.startswith(config["key"] + "info"):
        bot.sendMessage(chat_id, history(message.split(" ")[1]), parse_mode='Markdown')


def query(message):
    query_id, from_id, query_data = telepot.glance(message, flavor='callback_query')

    username = message["from"]["username"]
    rating = query_data
    meme_id: int = int(message["message"]["text"].split(" ")[8])

    if rating == "UpVote":
        rate_meme(int(meme_id), 1, username, True)
    elif rating == "DownVote":
        rate_meme(int(meme_id), -1, username, True)

    bot.answerCallbackQuery(query_id, text="thanks for your rating (" + rating + "/" + str(meme_id) + ")")


bot = telepot.Bot(config["tele_token"])

MessageLoop(bot, {'chat': handle,
                  'callback_query': query}).run_as_thread()
