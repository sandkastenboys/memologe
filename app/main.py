from config import config
from handler.Discord import DiscordAPI
from handler.Telegram import TelegramAPI

print("Starting Memologe ...")

if config["telegram_token"]:
    telegram: TelegramAPI = TelegramAPI()
    telegram.start()

if config["discord_token"]:
    discord: DiscordAPI = DiscordAPI()
    discord.run(config["discord_token"])
