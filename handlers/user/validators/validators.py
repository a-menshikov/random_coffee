import re
from datetime import datetime

from aiogram import types
from keyboards.user import (all_right_message, back_message, man_message,
                            skip_message, woman_message)
from loader import bot


def validate_name(message):
    """Валидация введенных данных в поле Имя"""
    return (re.fullmatch(
        r"^[a-яА-ЯЁёa-yA-Y\s]{1,100}$",
        message
    ) and len(message) <= 100)


async def validate_birthday(message: types.Message):
    """Валидация введенных данных в поле Дата рождения"""
    if re.fullmatch(
        r"^((0[1-9]|[12]\d)\.(0[1-9]|1[012])|"
        r"30\.(0[13-9]|1[012])|31\.(0[13578]|1[02]))\.(19|20)\d\d$",
        message.text
    ):
        date_obj = datetime.strptime(message.text, '%d.%m.%Y')
        difference = datetime.now() - date_obj
        age = int(difference.days) / 365
        if age < 0:
            await bot.send_message(
                message.from_user.id,
                'Вы что из будущего?)) Введите правильную дату рождения"'
            )
            return False
        elif age > 120:
            await bot.send_message(
                message.from_user.id,
                'Указанный возраст болеее 120 лет. '
                'Введите правильную дату рождения'
            )
            return False
        return True
    await bot.send_message(
        message.from_user.id,
        'Что то не так с введенными данными. '
        'Дата должно состоять из цифр и точек ДД.ММ.ГГГГ"'
    )
    return False


async def validate_about(message):
    """Валидация введенных данных в поле О себе"""
    if len(message.text) > 500:
        await bot.send_message(
            message.from_user.id,
            'Текст должен быть меньше 500 символов. Повторите ввод.'
        )
        return False
    return True


async def validate_gender(message: types.Message):
    """Валидация введенных данных в поле Пол пользователя"""
    choice = [man_message, woman_message, skip_message]
    if message.text not in choice:
        await bot.send_message(
            message.from_user.id,
            'Пожалуйста выберите из доступных вариантов или '
            'нажмите "Пропустить"'
        )
        return False
    return True


async def validate_check_info(message):
    """Валидация введенных данных при проверке выбора
    в форме подтверждения введенных данных"""
    choice = [all_right_message, back_message]
    if message.text not in choice:
        await bot.send_message(
            message.from_user.id,
            'Пожалуйста выберите из доступных вариантов.'
        )
        return False
    return True
