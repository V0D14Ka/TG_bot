from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, MessageCantBeDeleted, CantInitiateConversation
from create_bot import bot
from keyboard import kb_client
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from libs import get_weather, WalletParser
import re
from create_bot import db
from static import messages


# Машина состояний для погоды
class FSMweather(StatesGroup):
    place = State()


# Старт
async def commands_start(message: types.Message):
    if not db.is_user_exist(message.from_user.id):
        db.add_user(message.from_user.id)
        db.save()
    mesg = messages.welcome_mesg if message.text == '/start' or message.text == '!start' else messages.help_mesg
    sticker = open('static/welcome.webp', 'rb')
    try:
        if mesg == messages.welcome_mesg:
            await bot.send_sticker(message.from_user.id, sticker)
        await bot.send_message(message.from_user.id, mesg, reply_markup=kb_client)
        try:
            await message.delete()
        except MessageCantBeDeleted:
            pass
    except CantInitiateConversation:
        await message.reply(messages.cant_initiate_conversation)
    except BotBlocked:
        await message.reply(messages.bot_blocked)


# Записываем инфу о доходе/ расходе пользователя
async def record(message: types.Message):
    variants = (('/spent', '/s'), ('/earned', '/e'))
    operation = '-' if message.text.startswith(variants[0]) else '+'
    amount = message.text
    for i in variants:
        for j in i:
            amount = amount.replace(j, '').strip()
    if len(amount):
        x = re.findall(r"\d+(?:.\d+)?", amount)
        if len(x):
            amount = round(float(x[0].replace(',', '.')), 2)
            db.add_record(message.from_user.id, operation, amount)
            db.save()
            dic = {'-': 'расходе',
                   '+': 'доходе'}
            await message.reply(f"Запись о {dic[operation]} успешно внесена!")
        else:
            await message.reply('Не удалось определить сумму!')
    else:
        await message.reply('Не введена сумма!')


# Достаем историю за указанный период
async def history(message: types.Message):
    args = message.get_args()
    within = {
        "day": ('today', 'day', 'за сегодня', 'сегодня'),
        "month": ('month', 'за месяц', 'месяц'),
        "year": ('year', 'за год', 'год'),
        "*": ('all time', 'все время')
    }
    records, i = None, None
    for i in within:
        if args in within[i]:
            records = db.get_records(message.from_user.id, i)
            break

    if records is None:
        if not args:
            records = db.get_records(message.from_user.id)
            i = "*"
        else:
            await message.reply("Неккоректно указан период!")
            return

    if len(records):
        answer = f"🕘 История операций за {within[i][-1]}\n\n"
        for r in records:
            info = "➖ Расход" if not r[2] else "➕ Доход"
            answer += f"{info} - {r[3]} 🗓{r[4][0:10]}\n"
        await message.reply(answer)
    else:
        await message.reply("Записей не обнаружено!")


# Курс валют
async def command_wallet(message: types.Message):
    wallet = WalletParser()
    mesg = await message.reply(messages.waiting_request)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=mesg.message_id, text=wallet.get_currency())


# Погода
async def weather_start(message: types.Message):
    await FSMweather.place.set()
    await message.reply(messages.ask_for_place, reply_markup=ReplyKeyboardRemove())


async def weather_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place'] = message.text
        ans = get_weather(data['place'])
        await message.reply(ans)
        await state.finish()


async def weather(message: types.Message):
    place = message.text[7:]
    await message.reply(get_weather(place))


def register_handlers_client(_dp: Dispatcher):
    _dp.register_message_handler(commands_start, commands=['start', 'help'])
    _dp.register_message_handler(record, commands=['spent', 's', 'earned', 'e'])
    _dp.register_message_handler(history, commands=['history', 'h'])
    _dp.register_message_handler(command_wallet, lambda message: "курс валют" in message.text.lower())
    _dp.register_message_handler(weather_start, lambda message: message.text.lower() == 'погода', state=None)
    _dp.register_message_handler(weather_next, state=FSMweather.place)
    _dp.register_message_handler(weather, lambda message: message.text.lower().startswith('погода '))
