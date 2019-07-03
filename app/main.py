from config import config
from handler.Discord import Discord_API
print("Start Memologe ...")

if config["tele_token"] != "":
    import handler.Telegram
    pass
if config["disc_token"] == "":
    raise ValueError("Discord Token has to ben set")


# https://github.com/moby/moby/issues/30757

print("Run Memologe ...")

d: Discord_API = Discord_API()
d.run(config["disc_token"])
