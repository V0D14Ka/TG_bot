from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('Погода')
b2 = KeyboardButton('Курс валют')
b3 = KeyboardButton('Гороскоп')
inb1 = InlineKeyboardButton(text='🚗Транспорт🚗', callback_data='cat_1')
inb2 = InlineKeyboardButton(text='🍗Еда🍗', callback_data='cat_2')
inb3 = InlineKeyboardButton(text='🎒Образование🎒', callback_data='cat_3')
inb4 = InlineKeyboardButton(text='⌚Электроника и техника⌚', callback_data='cat_4')
inb5 = InlineKeyboardButton(text='🛰Интернет и связь🛰', callback_data='cat_5')
inb6 = InlineKeyboardButton(text='💎Подписки💎', callback_data='cat_6')
inb7 = InlineKeyboardButton(text='🏡Бытовые траты🏡', callback_data='cat_7')
inb8 = InlineKeyboardButton(text='💳Прочее💳', callback_data='cat_8')
inb9 = InlineKeyboardButton(text='❌ОТМЕНА❌', callback_data='cat_cancel')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
inkb_client = InlineKeyboardMarkup(row_width=1)

kb_client.add(b1).add(b2).add(b3)
inkb_client.add(inb1).add(inb2).add(inb3).add(inb4).add(inb5).add(inb6).add(inb7).add(inb8).add(inb9)
