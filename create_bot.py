import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB import BotDB
from libs import Parser, WeatherAPI

db = BotDB('sqlite.db')

storage = MemoryStorage()

parser = Parser()
weatherAPI = WeatherAPI()

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
