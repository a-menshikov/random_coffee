import sqlite3
from asyncio import sleep

from aiogram import types

from loader import bot, dp, logger


@dp.message_handler(commands=['check'])
async def check_message(message: types.Message):
    await sleep(10)
    for user in prepare_user_list():
        await send_message(
            teleg_id=user,
            text="Через несколько минут будем произведена рассылка"
        )


def prepare_user_list():
    conn = sqlite3.connect('data/coffee_database.db')

    cur = conn.execute("""SELECT user_info.teleg_id FROM user_status 
    JOIN user_info ON user_info.id = user_status.id 
    WHERE user_status.status = 1 """)
    data = cur.fetchall()
    return [element[0] for element in data]


async def send_message(teleg_id, **kwargs):
    try:
        await bot.send_message(teleg_id, **kwargs)
    except Exception as error:
        logger.error(f"Не возможно доставить сообщение пользователю  {teleg_id}. "
                     f"{error}")
        await change_status(teleg_id)


async def change_status(teleg_id):
    conn = sqlite3.connect('data/coffee_database.db')
    cur = conn.cursor()
    id_obj = cur.execute(
        """SELECT id FROM user_info WHERE teleg_id=?""", (teleg_id,)
    )
    teleg_id = id_obj.fetchone()[0]
    cur.execute(
        """UPDATE user_status SET status = 0
        WHERE id = ? """, (teleg_id,))
    conn.commit()
