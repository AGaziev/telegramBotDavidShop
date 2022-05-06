from aiogram.utils import executor
from create_bot import dp
from DatabaseHandler import totalUpdate as totalUpdateDB
from os import getenv

async def on_startup(_):
    print('Bot online!')


from handlers import client, admin, other

admin.register_handlers()
if getenv("mode") == "debug":
    client.register_handlers_debug()
else:
    client.register_handlers()
other.register_handlers()
totalUpdateDB()

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
