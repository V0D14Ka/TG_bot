from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, Unauthorized, MessageCantBeDeleted, CantInitiateConversation
from create_bot import bot
from keyboard import kb_client
from create_bot import db
from static import messages


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


def register_handlers_client_main(_dp: Dispatcher):
    _dp.register_message_handler(commands_start, commands=['start', 'help'])
    _dp.register_message_handler(record, commands=['spent', 's', 'earned', 'e'])
    _dp.register_message_handler(history, commands=['history', 'h'])
