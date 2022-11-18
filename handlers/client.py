from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, MessageCantBeDeleted
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
async def commands_start(message: types.Message):
    sticker = open('static/welcome.webp', 'rb')
    welcome_mesg = "Приветствую!Меня зовут AboBot!\nЯ могу узнавать погоду и актуальный курс валют!"
    help_mesg = "Помощь:\n🔘Узнать погоду: 'Погода город' или 'Погода'.\n🔘Узнать актуальный курс валют : 'Курс " \
                "валют'. "
    mesg = welcome_mesg if message.text == '/start' else help_mesg
    try:
        if mesg == welcome_mesg:
            await bot.send_sticker(message.from_user.id, sticker)
        await bot.send_message(message.from_user.id, mesg, reply_markup=kb_client)
        try:
            await message.delete()
        except MessageCantBeDeleted:
            print('Cant delete, not a administrator')
    except ChatNotFound:
        await message.reply("Для начала работы со мной напишите мне в ЛС!")
    except BotBlocked:
        await message.reply("Разблокируйте меня, чтобы продолжить диалог!")


# Курс валют
async def command_wallet(message: types.Message):
    wallet = WalletParser()
    mesg = await message.reply('Запрос выполняется, подождите...🕒')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=mesg.message_id, text=wallet.get_currency())


# Погода
async def weather_start(message: types.Message):
    await FSMweather.place.set()
    await message.reply('Чтобы узнать погоду напишите место!🌍', reply_markup=ReplyKeyboardRemove())


async def weather_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place'] = message.text
        ans = get_weather(data['place'])
        await message.reply(ans)
        await state.finish()


async def weather(message: types.Message):
    place = message.text[7:]
    # print(place)
    await message.reply(get_weather(place))


def register_handlers_client(_dp: Dispatcher):
    _dp.register_message_handler(commands_start, commands=['start', 'help'])
    _dp.register_message_handler(command_wallet, lambda message: "курс валют" in message.text.lower())
    _dp.register_message_handler(weather_start, lambda message: message.text.lower() == 'погода', state=None)
    _dp.register_message_handler(weather_next, state=FSMweather.place)
    _dp.register_message_handler(weather, lambda message: message.text.lower().startswith('погода '))
