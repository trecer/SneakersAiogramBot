from aiogram import Bot, Dispatcher, types
from app import keyboards as kb
from app import database as db
from aiogram.utils import executor
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAMNZQwXWT6dILmr7PmsUtDZF2mL93EAAgUAA8A2TxP5al-agmtNdTAE')
    await message.answer(f'{message.from_user.first_name}, Добро пожаловать в магазин кроссовок!',
                         reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизировались как администратор',
                             reply_markup=kb.main_admin)


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Каталог пуст!', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста!')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товары у него: @Urii_Logachev')


@dp.message_handler(text='Админ-панель')
async def open_admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 't-shirt':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Вы выбрали футболки')
    elif callback_query.data == 'shorts':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Вы выбрали шорты')
    elif callback_query.data == 'sneakers':    
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Вы выбрали кроссовки')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

