from aiogram.utils import executor
from create_bot import dp

import os


async def on_startup(_):
    print('Bot online!')


from handlers import client, admin, other

admin.register_handlers()
client.register_handlers()
other.register_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
