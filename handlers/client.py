from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from create_bot import bot
from keyboard import kb_client
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from libs import get_weather, WalletParser


# Машина состояний для погоды
class FSMweather(StatesGroup):
    place = State()


# Старт
async def command_start(message: types.Message):
    try:
        sticker = open('static/welcome.webp', 'rb')
        await bot.send_sticker(message.from_user.id, sticker)
        await bot.send_message(message.from_user.id, "Приветствую!Меня зовут AboBot!\nЯ могу узнавать погоду и "
                                                     "актуальный курс валют!.",
                               reply_markup=kb_client)
        await message.delete()
    except ChatNotFound:
        await message.reply("Для начала работы со мной напишите мне в ЛС!")
    except BotBlocked:
        await message.reply("Разблокируйте меня, чтобы продолжить диалог!")


# Курс валют
async def command_wallet(message: types.Message):
    wallet = WalletParser()
    await message.reply(wallet.get_currency())


# Погода
async def weather_start(message: types.Message):
    await FSMweather.place.set()
    await message.reply('Чтобы узнать погоду напишите место!🌍', reply_markup=ReplyKeyboardRemove())


async def weather_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place'] = message.text
        ans = get_weather(data['place'])
        await message.reply(ans, reply_markup=kb_client)
        await state.finish()


def register_handlers_client(_dp: Dispatcher):
    _dp.register_message_handler(command_start, commands=['start', 'help'])
    _dp.register_message_handler(command_wallet, commands=['Курс_валют'])
    _dp.register_message_handler(weather_start, commands=['Погода'], state=None)
    _dp.register_message_handler(weather_next, state=FSMweather.place)
