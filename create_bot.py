import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv


load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)
