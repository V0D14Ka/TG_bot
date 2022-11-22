from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Погода')
b2 = KeyboardButton('Курс валют')
b3 = KeyboardButton('Гороскоп')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3)
