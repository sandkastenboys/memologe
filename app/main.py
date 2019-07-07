from config import config
from handler.Discord import DiscordAPI
from handler.Telegram import init_telegram

print("Starting Memologe ...")

if config["telegram_token"]:
    init_telegram()

if config["discord_token"]:
    discord: DiscordAPI = DiscordAPI()
    discord.run(config["discord_token"])
