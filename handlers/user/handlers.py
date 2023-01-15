from aiogram import types

from loader import bot, dp, db_controller, logger

from keyboards.user import *
from handlers.user.new_member import get_gender_from_db, start_registration


@dp.message_handler(text=menu_message)
async def main_menu(message: types.Message):
    """Вывод меню"""
    await bot.send_message(
        message.from_user.id,
        text="Меню:",
        reply_markup=main_markup()
    )


@dp.callback_query_handler(text=my_profile_message)
async def send_profile(message: types.Message):
    """Вывод данных о пользователе"""
    logger.info(f"Пользователь с TG_ID {message.from_user.id} "
                f"запросил информацию о себе")
    data = dict(get_user_data_from_db(message.from_user.id))
    if data['about'] == 'null':
        data['about'] = 'Не указано'
    gender_id = data['gender']
    gender_status = get_gender_from_db(gender_id)
    data['gender'] = gender_status
    birthday = data['birthday'].split('-')
    birthday.reverse()
    data['birthday'] = '-'.join(birthday)
    await bot.send_message(
        message.from_user.id,
        f"Имя: {data['name']};\n"
        f"Дата рождения: {data['birthday']};\n"
        f"О себе: {data['about']};\n"
        f"Пол: {data['gender']};",
        reply_markup=edit_profile_markup()
    )


def get_user_data_from_db(teleg_id):
    """Получение id пользователя"""
    query = """SELECT * FROM user_info WHERE teleg_id=?"""
    values = (teleg_id,)
    row = db_controller.row_factory(query, values)
    return row.fetchone()


def get_user_status_from_db(user_id):
    """Получение статуса участия пользователя из БД"""
    query = """SELECT * FROM user_status WHERE id=?"""
    values = (user_id,)
    row = db_controller.row_factory(query, values)
    return row.fetchone()


def get_holidays_status_from_db(user_id):
    """Получение статуса каникул пользователя из БД"""
    query = """SELECT * FROM holidays_status WHERE id=?"""
    values = (user_id,)
    row = db_controller.row_factory(query, values)
    return row.fetchone()


@dp.callback_query_handler(text=edit_profile_message)
async def edit_profile(message: types.Message):
    """Перенаправление на повторную регистрацию"""
    logger.info(f"Пользователь с TG_ID {message.from_user.id} "
                f"отправлен на повторную регистрацию")
    await start_registration(message)


@dp.callback_query_handler(text=about_bot_message)
async def about_bot_message(message: types.Message):
    """Вывод информации о боте"""
    logger.info(f"Пользователь с TG_ID {message.from_user.id} "
                f"запросил информацию о боте")
    await bot.send_message(
        message.from_user.id,
        "Тут будет сообщение о боте"
    )


@dp.callback_query_handler(text=my_status_message)
async def status_message(message: types.Message):
    """Вывод статуса участия в распределении"""
    logger.info(f"Пользователь с TG_ID {message.from_user.id} " 
                f"запросил информацию о статусе участия")
    user_row = get_user_data_from_db(message.from_user.id)
    status_row = get_user_status_from_db(user_row['id'])
    if status_row['status'] == 1:
        status = "Вы участвуете в распределении на следующец неделе"
    else:
        holidays_row = get_holidays_status_from_db(user_row['id'])
        holidays_till = holidays_row['till_date'].split('-')
        holidays_till.reverse()
        holidays_till = '-'.join(holidays_till)
        status = f"Вы на каникулах до {holidays_till}"
    await bot.send_message(message.from_user.id, text=status)
    logger.info(f"Пользователь с TG_ID {message.from_user.id} "
                f"получил информацию о статусе участия")
