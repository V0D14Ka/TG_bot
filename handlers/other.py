import string
import json
from aiogram import types, Dispatcher
from create_bot import bot, db


async def send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply("Ругательства запрещены!")
        try:
            await message.delete()
        except:
            pass


def register_handlers_other(_dp: Dispatcher):
    _dp.register_message_handler(send)
