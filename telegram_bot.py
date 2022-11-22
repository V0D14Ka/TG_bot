from create_bot import dp
from aiogram.utils import executor
from handlers import mainpart, extrapart, other

mainpart.register_handlers_client_main(dp)
extrapart.register_handlers_client_extra(dp)
other.register_handlers_other(dp)


async def on_startup(_):
    print("Бот успешно запущен")


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
