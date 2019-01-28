import telepot
from config import config
from telepot.loop import MessageLoop
from Memologe.MySql_DB import db
import random
import time


# https://telepot.readthedocs.io/en/latest/
def handle(message):
    print(message)
    content_type, chat_type, chat_id = telepot.glance(message)
    print(content_type, chat_type, chat_id, message["text"])

    message = message["text"].split(" ")
    if chat_type == "supergroup":
        message[0] = "$" + message[0][1:]

    if message[0] == config["key"] + 'ran_meme':

        try:
            how_many = int(message[1])
            if how_many > 10:
                how_many = 10
        except:
            how_many = 1

        for x in range(how_many):
            ran_id = random.randint(0, db.max_id())

            meme = db.get_meme_by_id(ran_id)
            print(meme)
            bot.sendMessage(chat_id, meme[1])

    if message[0] == config["key"] + 'help':
        bot.sendMessage(chat_id,
                        'Memologe Commands Telegram:\n$ran_meme <how_many> posts random meme\n$search <tag> <how_many = 1> searches memes based on tag\n$size amount of memes in the db')

    if message[0] == config["key"] + "size":
        size = db.size_of_db()

        bot.sendMessage(chat_id, "There are : " + str(size[0][0]) + " memes in the database")

    if message[0] == config["key"] + "search":
        tag = message[1]
        try:
            how_may = int(message[2])
        except:
            how_may = 1

        data = db.search_meme(tag)

        if data == []:
            bot.sendMessage(chat_id, "Sry no meme was found with this tag")

        random.shuffle(data)

        for x in range(how_may):
            try:
                bot.sendMessage(chat_id, data[x][1])
            except:
                break

    if message[0] == config["key"] + "tags":
        bot.sendMessage(chat_id, "\n".join(db.tags))


bot = telepot.Bot(config["tele_token"])

MessageLoop(bot, handle).run_as_thread()
