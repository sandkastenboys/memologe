from config import config

print("Read Config")

if config["tele_token"] != "":
    pass
    #import Telegram

if config["disc_token"] == "":
    raise ValueError("Discord Token has to ben set")

from Discord.Discord_Class import Discord_API
#https://github.com/moby/moby/issues/30757

print("Run Memologe ...")

d = Discord_API()
d.run(config["disc_token"])
