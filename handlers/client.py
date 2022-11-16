from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from create_bot import bot


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Добрый день")
        await message.delete()
    except ChatNotFound:
        await message.reply("Для начала работы со мной напишите мне в ЛС!")
    except BotBlocked:
        await message.reply("Разблокируйте меня, чтобы продолжить диалог!")


def register_handlers_client(_dp: Dispatcher):
    _dp.register_message_handler(command_start, commands=['start', 'help'])
