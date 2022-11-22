from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, Unauthorized, MessageCantBeDeleted, CantInitiateConversation
from create_bot import bot
from keyboard import kb_client
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import db, parser, weatherAPI
from static import messages


# Машина состояний для погоды
class FSMweather(StatesGroup):
    place = State()


# Машина состояний для гороскопа
class FSMhoroscope(StatesGroup):
    sign = State()


# Старт
async def commands_start(message: types.Message):
    if not db.is_user_exist(message.from_user.id):
        db.add_user(message.from_user.id)
        db.save()
    mesg = messages.welcome_mesg if message.get_command() == '/start' else messages.help_mesg
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
    except Unauthorized:
        await message.reply(messages.unauthorized)


# Записываем инфу о доходе/ расходе пользователя
async def record(message: types.Message):
    if not db.is_user_exist(message.from_user.id):

        await message.reply(messages.reg)
        return
    variants = (('/spent', '/s'), ('/earned', '/e'))
    dic = {'-': 'расходе', '+': 'доходе'}
    operation = '-' if message.get_command() in variants[0] else '+'
    amount = message.get_args().replace(',', '.')
    if not amount.replace('.', '').isdigit():
        await message.reply(messages.not_a_digit)
        return
    amount = round(float(amount), 2)
    db.add_record(message.from_user.id, operation, amount)
    db.save()
    await message.reply(f"Запись о {dic[operation]} успешно внесена!")


# Достаем историю за указанный период
async def history(message: types.Message):
    if not db.is_user_exist(message.from_user.id):
        await message.reply(messages.reg)
        return
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
            await message.reply(messages.not_period)
            return

    if len(records):
        answer = f"🕘 История операций за {within[i][-1]}\n\n"
        for r in records:
            info = "➖ Расход" if not r[2] else "➕ Доход "
            answer += f"{info} 🗓({r[4][0:10]}) - {r[3]}₽ \n"
        await message.reply(answer)
    else:
        await message.reply(messages.empty_h)


# Курс валют
async def command_wallet(message: types.Message):
    mesg = await message.reply(messages.waiting_request)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=mesg.message_id, text=parser.get_currency())


# гороскоп
async def horoscope_start(message: types.Message):
    await FSMhoroscope.sign.set()
    await message.reply(messages.ask_for_sign, reply_markup=ReplyKeyboardRemove())


async def horoscope_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sign'] = message.text.lower()
        mesg = await message.reply(messages.waiting_request)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=mesg.message_id,
                                    text=parser.get_horoscope(data['sign']))
        await state.finish()


async def horoscope(message: types.Message):
    sign = message.text[9:].lower()
    mesg = await message.reply(messages.waiting_request)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=mesg.message_id,
                                text=parser.get_horoscope(sign))


# Погода
async def weather_start(message: types.Message):
    await FSMweather.place.set()
    await message.reply(messages.ask_for_place, reply_markup=ReplyKeyboardRemove())


async def weather_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place'] = message.text
        ans = weatherAPI.get_weather(data['place'])
        await message.reply(ans)
        await state.finish()


async def weather(message: types.Message):
    place = message.text[7:]
    await message.reply(weatherAPI.get_weather(place))


def register_handlers_client(_dp: Dispatcher):
    _dp.register_message_handler(commands_start, commands=['start', 'help'])
    _dp.register_message_handler(record, commands=['spent', 's', 'earned', 'e'])
    _dp.register_message_handler(history, commands=['history', 'h'])
    # FSM horoscope
    _dp.register_message_handler(horoscope_start, lambda message: message.text.lower() == 'гороскоп', state=None)
    _dp.register_message_handler(horoscope_next, state=FSMhoroscope.sign)
    # FSM weather
    _dp.register_message_handler(weather_start, lambda message: message.text.lower() == 'погода', state=None)
    _dp.register_message_handler(weather_next, state=FSMweather.place)
    # one-request funcs
    _dp.register_message_handler(horoscope, lambda message: message.text.lower().startswith('гороскоп '))
    _dp.register_message_handler(weather, lambda message: message.text.lower().startswith('погода '))
    _dp.register_message_handler(command_wallet, lambda message: "курс валют" in message.text.lower())
