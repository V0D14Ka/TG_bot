from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, Unauthorized, MessageCantBeDeleted, CantInitiateConversation
from create_bot import bot
from keyboard import kb_client
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import db, parser, weatherAPI, GPT
from static import messages


# Машина состояний для погоды
class FSMweather(StatesGroup):
    place = State()


# Машина состояний для гороскопа
class FSMhoroscope(StatesGroup):
    sign = State()


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


async def command_wallet(message: types.Message):
    mesg = await message.reply(messages.waiting_request)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=mesg.message_id, text=parser.get_currency())


async def gpt(message: types.Message):
    mesg = await message.reply(messages.waiting_request)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=mesg.message_id,
                                text=GPT.check_gpt(message.get_args()))


def register_handlers_client_extra(_dp: Dispatcher):
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
    # chatGPT
    _dp.register_message_handler(gpt, commands=['gpt'])
