# start
welcome_mesg = '''Приветствую, меня зовут 🦾AboBot🦾!
Я могу стать вашим финансовым ассистентом!
Буду запоминать ваши расходы и доходы, анализировать их!
Чтобы узнать как со мной взаимодействовать, напишите: /help'''
help_mesg = '''⭕Помощь:⭕
💰 Внести сведения о доходе: '/e сумма'.💰
    Пример: '/e 500' 
💰 Внести сведения о расходе: '/s сумма'.💰
    Пример: '/s 150'
💎 Список операций за период: '/h период'.💎
    Примеры:
    🎯'/h сегодня' - все операции за текущий день,
    🎯'/h месяц' - все операции за последние 30 дней,
    🎯'/h' - все операции за все время.
🌍А так же дополнительные функции:🌍
    🔘Гороскоп: 'Гороскоп знак' или 'Гороскоп'.
    🔘Погода: 'Погода город' или 'Погода'.
    🔘Курс валют: 'Курс валют'.
'''

# reply exceptions
cant_initiate_conversation = '''Для начала работы со мной напишите мне в ЛС!'''
bot_blocked = "Разблокируйте меня, чтобы продолжить диалог!"
unauthorized = 'Не удалось написать вам!'
went_wrong = 'Что-то пошло не так...'

# waiting for input
waiting_request = 'Запрос выполняется, подождите...🕒'
ask_for_place = 'Чтобы узнать погоду напишите место!🌍'
ask_for_sign = 'Чтобы узнать гороскоп напишите знак зодиака!☯'
ask_for_cat = 'Выберите категорию траты:'

# incorrect input
not_period = "Неккоректно указан период!"
not_a_digit = 'Не удалось определить сумму!'
not_a_place = 'Неккоректный город!😡'
not_a_sign = 'Нет такого знака зодиака!'

# register
reg = 'Дня начала зарегистрируйтесь: /start'

# empty history
empty_h = "Записей не обнаружено!"

# weather
weather_info = '''Сейчас в населенном пункте - %s🏙:
❄ Температура воздуха: %s°C.
🤨 Ощущается как: %s°C.
✅ Статус: %s.
💨 Порывы ветра достигают: %sм/с.'''

# parser
wallet = '''Текущий курс валют:
🇺🇸 1$ = %s₽ 🇷🇺
🇪🇺 1€ = %s₽ 🇷🇺'''

# record
succesful_spent = '''✅Запись о расходе успешно внесена!✅
Категория: %s'''
succesful_earned = '✅Запись о доходе успешно внесена!✅'
cancel = 'Операция отменена!❌'

final = '''✔Потрачено за период: %s₽.
✔Заработано за период: %s₽.
🏆Итог %s%s₽.🏆\n'''
