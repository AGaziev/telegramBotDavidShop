from aiogram.utils import executor
from create_bot import dp
from DatabaseHandler import totalUpdate as totalUpdateDB
from os import getenv

async def on_startup(_):
    print('Bot online!')


from handlers import client, admin, other, sideSeller

admin.registerHandlers()
sideSeller.registerHandlers()
if getenv("mode") == "debug":
    client.registerHandlersDebug()
    other.registerHandlers()
else:
    client.registerHandlers()
totalUpdateDB()

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
