from aiogram.utils import executor
from create_bot import dp
from DatabaseHandler import totalUpdate as totalUpdateDB

import os


async def on_startup(_):
    print('Bot online!')


from handlers import client, admin, other

admin.register_handlers()
client.register_handlers()
other.register_handlers(dp)
totalUpdateDB()

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
