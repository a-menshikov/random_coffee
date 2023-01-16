import sqlite3

from data import ADMIN_TG_ID
from handlers.user.ban_check import check_user_in_ban
from loader import bot, dp, logger
from aiogram import executor, types
import aioschedule
import asyncio
from datetime import datetime
from controllerBD import DatabaseManager
from keyboards import *
from states import UserData, AdminData, BannedState
from handlers.user import *
from handlers.admin import *
from match_algoritm import MachingHelper


@dp.message_handler(commands=['start', 'help'], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    """Функция первого обращения к боту."""
    await state.reset_state()
    name = message.from_user.full_name
    logger.info(f"user id-{message.from_user.id} tg-@{message.from_user.username} start a bot")
    await bot.send_message(
        message.from_user.id,
        text=f'Привет, {name}. У нас вот такой бот. "Регламент".',
    )
    await check_and_add_registration_button(message)


@dp.message_handler(text=algo_start, state=AdminData.start)
async def start_algoritm(message: types.Message, state: FSMContext):
    await check_message(state)
    mc.prepare()
    res = mc.start()
    print("retunr-",res)
    await mc.send_and_write(res)


async def check_and_add_registration_button(message: types.Message):
    if message.from_user.id == int(ADMIN_TG_ID):
        await bot.send_message(
            message.from_user.id,
            text="Привет, Админ. Добро пожаловать в меню администратора",
            reply_markup=admin_main_markup(),
        )
    elif not await check_user_in_base(message):
            await bot.send_message(
                message.from_user.id,
                text="Нажмите кнопку регистрации для старта.",
                reply_markup=start_registr_markup()
            )
            await UserData.start.set()

    else:
        if not await check_user_in_ban(message):
            await bot.send_message(
                message.from_user.id,
                text="Нажмите кнопку меню и выберите из доступных вариантов",
                reply_markup=main_markup(),
            )
        else:
            await bot.send_message(
                message.from_user.id,
                text="К сожалению вы нарушили наши правила и попали в бан. "
                     "Для решения данного вопроса просим обратиться к "
                     "администратору",
            )
            await BannedState.start.set()

async def scheduler():
    aioschedule.every().day.at("23:19").do(sheduled_check_holidays)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())

if __name__ == '__main__':
    mc = MachingHelper()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

