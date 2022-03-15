from create_bot import bot, dp
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

adminId = {'david': '1256578670', 'alan': '292667494'}


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    type = State()
    category = State()
    price = State()


@dp.message_handler(commands='admin', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id in adminId.values():

    else:
        await message.reply('Недостаточно прав')


@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await


async def admin_panel(message):
    


def register_handlers_client(dp: Dispatcher):
    pass
