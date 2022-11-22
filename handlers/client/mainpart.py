from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked, Unauthorized, MessageCantBeDeleted, CantInitiateConversation
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from keyboard import kb_client, inkb_client
from create_bot import db
from static import messages


# FSM для записи расхода
class FSMrecord(StatesGroup):
    cat = State()


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
async def record(message: types.Message, state: FSMContext):
    if not db.is_user_exist(message.from_user.id):
        await message.reply(messages.reg)
        return
    async with state.proxy() as data:
        variants = (('/spent', '/s'), ('/earned', '/e'))
        operation = '-' if message.get_command() in variants[0] else '+'
        amount = message.get_args().replace(',', '.')
        if not amount.replace('.', '').isdigit() or amount[0] in "0,.":
            await message.reply(messages.not_a_digit)
            return
        amount = round(float(amount), 2)
        data['amount'] = amount
        data['operation'] = operation
        data['user_id'] = message.from_user.id
        if operation == '-':
            await FSMrecord.cat.set()
            mesg = await message.reply(messages.ask_for_cat, reply_markup=inkb_client)
            data['mesg'] = mesg
        else:
            db.add_record(data['user_id'], data['operation'], data['amount'])
            db.save()
            await message.reply(messages.succesful_earned)


async def category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        dic = {
            '1': 'Транспорт',
            '2': 'Еда',
            '3': 'Образование',
            '4': 'Электроника и техника',
            '5': 'Бытовые траты',
            '6': 'Прочее',
        }
        data['cat'] = str(callback.data.split('_')[1])
        if data['cat'] == 'cancel':
            await callback.answer()
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text=messages.cancel, reply_markup=None)
            await state.finish()
            return
        db.add_record(data['user_id'], data['operation'], data['amount'], data['cat'])
        db.save()
        await callback.answer()
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text=messages.succesful_spent % dic[data['cat']], reply_markup=None)
        await state.finish()


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
        minus = 0
        plus = 0

        answer = f"🕘 История операций за {within[i][-1]}:\n"
        ans2 = ""
        for r in records:
            if not r[2]:
                info = "➖ Расход"
                minus += int(r[3])
            else:
                info = "➕ Доход "
                plus += int(r[3])
            ans2 += f"{info} 🗓({r[4][0:10]}) - {r[3]}₽ \n"
        total = '+' if plus > minus else '-'
        answer += messages.final % (str(minus), str(plus), total, abs(plus-minus)) + ans2
        await message.reply(answer)
    else:
        await message.reply(messages.empty_h)


def register_handlers_client_main(_dp: Dispatcher):
    _dp.register_message_handler(commands_start, commands=['start', 'help'])
    _dp.register_message_handler(callback=record, commands=['spent', 's', 'earned', 'e'], state=None)
    _dp.register_callback_query_handler(callback=category, text_contains='cat_', state=FSMrecord.cat)
    _dp.register_message_handler(history, commands=['history', 'h'])
