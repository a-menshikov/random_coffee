from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from data import ADMIN_TG_ID
from handlers.user.get_info_from_table import check_user_in_base
from handlers.user.ban_check import check_user_in_ban
from keyboards.admin import admin_main_markup
from keyboards.user import start_registr_markup, menu_markup
from loader import bot
from states import UserData, BannedState


async def check_and_add_registration_button(message: types.Message):
    """Проверка пользователя для последующих действий."""
    if not await check_user_in_base(message):
        name = message.from_user.full_name
        await bot.send_message(
            message.from_user.id,
            text=(f"Добро пожаловать в бот, {name}!\n\n"
                  f"Для подбора пары нужно пройти небольшую регистрацию: "
                  f"представиться и ответить на пару вопросов о себе, "
                  f"чтобы собеседнику было проще начать с тобой разговор. Если"
                  f" отвечать не хочется, то часть шагов можно пропустить.\n\n"
                  f"Нажми кнопку \"Регистрация\" ниже.\n\n"
                  f"Для общения, помощи и рассказов о том, как прошла "
                  f"встреча присоединяйся к уютному сообществу бота в "
                  f"телеграм https://t.me/+Ai1RweqsyjFhNmFi"
                  ),
            reply_markup=start_registr_markup()
        )
        await UserData.start.set()
    elif message.from_user.id in list(map(int, ADMIN_TG_ID.split())):
        await bot.send_message(
            message.from_user.id,
            text="Привет, Админ. Добро пожаловать в меню администратора",
            reply_markup=admin_main_markup(),
        )
    else:
        if not await check_user_in_ban(message):
            await bot.send_message(
                message.from_user.id,
                text="Воспользуйтесь меню",
                reply_markup=menu_markup(message),
            )
        else:
            await bot.send_message(
                message.from_user.id,
                text="К сожалению вы нарушили наши правила и попали в бан. "
                     "Для решения данного вопроса просим обратиться к "
                     "администратору @Loravel",
                reply_markup=ReplyKeyboardRemove()
            )
            await BannedState.start.set()
