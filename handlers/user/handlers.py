import sqlite3

from aiogram import types

from data.config import dp, bot

from aiogram.utils.markdown import hlink


def check_user_in_base(message):
    """Проверяем пользователя на наличие в БД."""
    conn = sqlite3.connect('data/coffee_database.db')
    cur = conn.cursor()
    info = cur.execute(
        """SELECT * FROM user_info WHERE teleg_id=?""", (message.from_user.id,)
    )
    if info.fetchone() is None:
        # Делаем когда нету человека в бд
        return False
    return True

def change_status_to_yes(message: types.Message):
    conn = sqlite3.connect('data/coffee_database.db')
    cur = conn.cursor()
    cur.execute("""update user_status SET status = ? where id = (
        SELECT id FROM user_info WHERE teleg_id = ?
    )""", (
        1, message.from_user.id
    ))
    conn.commit()


def change_take_part_status_to_no(message: types.Message):
    conn = sqlite3.connect('random_coffee.db')
    cur = conn.cursor()
    cur.execute("""update users SET take_part = ? where tg_id = ?""", (
        0, message.from_user.id
    ))
    conn.commit()



def get_data_from_db_for_mailing_list():
    conn = sqlite3.connect('random_coffee.db')

    cur = conn.execute("""SELECT tg_id FROM users where holidays = 0 and take_part = 0""")
    data = cur.fetchall()
    return [element[0] for element in data]

@dp.message_handler(commands=['send'])
async def send(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f'<a href="tg://user?id={message.from_user.id}">Alex</a>',
        parse_mode="HTML"
    )
